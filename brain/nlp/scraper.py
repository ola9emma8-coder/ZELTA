# nlp/scraper.py

import asyncio
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin

import aiohttp
from bs4 import BeautifulSoup


class ZeltaNewsScraper:
    """
    Nigerian financial news scraper for ZELTA.

    Purpose:
    - Fetch relevant headlines from Nigerian finance/news sources
    - Normalize and deduplicate titles
    - Return a clean in-memory payload for nlp/scorer.py

    Notes:
    - This file only ingests news.
    - Do not score sentiment here.
    - Keep this module focused on data collection.
    """

    def __init__(self, session: aiohttp.ClientSession, max_items_per_site: int = 10):
        self.session = session
        self.max_items_per_site = max_items_per_site

        # Site config: keep this easy to extend.
        # If a selector stops working, update only this map.
        self.site_map = {
            "nairametrics": {
                "url": "https://nairametrics.com/category/financial-news/",
                "item_selector": "article, div.td_module_wrap, div.td-module-container",
                "title_selector": "h1, h2, h3",
                "link_selector": "a",
            },
            "businessday": {
                "url": "https://businessday.ng/category/news/economy/",
                "item_selector": "article",
                "title_selector": "h1, h2, h3",
                "link_selector": "a",
            },
            "punch": {
                "url": "https://punchng.com/topics/business/",
                "item_selector": "article, div.post-content, div.entry-content",
                "title_selector": "h1, h2, h3",
                "link_selector": "a",
            },
        }

        # Used for clean deduplication across sources
        self.seen_titles = set()

        # Updated relevance hints for Nigerian campus/macro context
        # Incorporates the core macro terms + OAU student specific stress amplifiers
        self.relevant_keywords = {
            "naira", "usd", "dollar", "fx", "inflation", "cbn", "interest rate",
            "economy", "recession", "policy", "exchange rate", "devalue",
            "economics", "bank", "market", "prices", "forex",
            # Campus Amplifiers (Crucial for the OAU student context)
            "asuu", "strike", "tuition", "hostel", "oau", "student", "cost of living"
        }

    async def fetch_page(self, url: str) -> Optional[str]:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            )
        }

        try:
            async with self.session.get(url, headers=headers, timeout=aiohttp.ClientTimeout(total=20)) as resp:
                if resp.status != 200:
                    return None
                return await resp.text()
        except Exception:
            return None

    def normalize_title(self, title: str) -> str:
        return " ".join(title.lower().split()).strip()

    def is_relevant(self, title: str) -> bool:
        """
        Lightweight relevance filter for MVP.
        This is intentionally simple; scorer.py will do the real NLP work.
        """
        t = title.lower()
        return any(keyword in t for keyword in self.relevant_keywords)

    def build_absolute_url(self, base_url: str, link: str) -> str:
        if not link:
            return base_url
        return urljoin(base_url, link)

    def extract_items(self, html: str, source_name: str, source_url: str, cfg: Dict[str, Any]) -> List[Dict[str, Any]]:
        soup = BeautifulSoup(html, "html.parser")
        items: List[Dict[str, Any]] = []

        for block in soup.select(cfg["item_selector"]):
            title_tag = block.select_one(cfg["title_selector"])
            if not title_tag:
                continue

            title = title_tag.get_text(" ", strip=True)
            if not title:
                continue

            normalized = self.normalize_title(title)

            # Deduplicate across all sites
            if normalized in self.seen_titles:
                continue

            # Keep the feed more useful for NLP
            # You can remove this later if you want broader coverage.
            if not self.is_relevant(title):
                continue

            link_tag = block.select_one(cfg["link_selector"])
            link = link_tag.get("href") if link_tag and link_tag.get("href") else source_url
            link = self.build_absolute_url(source_url, link)

            self.seen_titles.add(normalized)

            items.append(
                {
                    "source": source_name,
                    "title": title,
                    "url": link,
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }
            )

            if len(items) >= self.max_items_per_site:
                break

        return items

    async def fetch_site(self, name: str, cfg: Dict[str, Any]) -> List[Dict[str, Any]]:
        html = await self.fetch_page(cfg["url"])
        if not html:
            return []

        try:
            return self.extract_items(html, name, cfg["url"], cfg)
        except Exception:
            return []

    async def get_payload(self) -> List[Dict[str, Any]]:
        tasks = [
            self.fetch_site(name, cfg)
            for name, cfg in self.site_map.items()
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        payload: List[Dict[str, Any]] = []
        for result in results:
            if isinstance(result, Exception):
                continue
            payload.extend(result)

        # Optional: newest first
        payload.sort(key=lambda x: x["timestamp"], reverse=True)
        return payload


async def run_scraper() -> List[Dict[str, Any]]:
    """
    Entry point for Day 2 pipeline.
    Returns a list of news headline dictionaries.
    """
    async with aiohttp.ClientSession() as session:
        scraper = ZeltaNewsScraper(session=session, max_items_per_site=10)
        payload = await scraper.get_payload()
        print(f"Captured {len(payload)} relevant Nigerian financial headlines.")
        return payload


if __name__ == "__main__":
    asyncio.run(run_scraper())