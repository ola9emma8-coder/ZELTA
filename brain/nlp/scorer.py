# nlp/scorer.py

from typing import List, Dict, Any
import numpy as np

from transformers import pipeline


class ZeltaSentimentScorer:
    """
    NLP Sentiment Engine for ZELTA

    Purpose:
    - Take news headlines
    - Run sentiment analysis using RoBERTa
    - Output structured sentiment scores with Campus Amplification

    This feeds into:
    → stress/index.py
    """

    def __init__(self):
        # Lightweight, good for finance/news sentiment.
        # (Optimized for deployment on Google Cloud Run / Vertex AI)
        self.model_name = "cardiffnlp/twitter-roberta-base-sentiment"

        self.sentiment_pipeline = pipeline(
            "sentiment-analysis",
            model=self.model_name,
            tokenizer=self.model_name
        )

        # Map model output to numeric values
        self.label_map = {
            "LABEL_0": -1.0,  # negative
            "LABEL_1": 0.0,  # neutral
            "LABEL_2": 1.0  # positive
        }

        # Campus specific keywords that severely impact OAU student financial stress
        self.campus_amplifiers = ["asuu", "strike", "tuition", "hostel", "oau", "fee", "student"]

    def score_headline(self, item: Dict[str, Any]) -> Dict[str, Any]:
        title = item.get("title", "")
        title_lower = title.lower()

        # Detect if this headline directly impacts the student's immediate ecosystem
        is_campus_relevant = any(amp in title_lower for amp in self.campus_amplifiers)

        # Apply a 1.5x multiplier to the mathematical weight if it's a campus issue
        weight = 1.5 if is_campus_relevant else 1.0

        try:
            result = self.sentiment_pipeline(title)[0]
            label = result["label"]
            confidence = result["score"]

            sentiment_value = self.label_map.get(label, 0.0)

            return {
                **item,
                "sentiment": sentiment_value,
                "confidence": confidence,
                "sentiment_label": self._label_name(sentiment_value),
                "is_campus_relevant": is_campus_relevant,
                "weight": weight
            }

        except Exception:
            return {
                **item,
                "sentiment": 0.0,
                "confidence": 0.0,
                "sentiment_label": "neutral",
                "is_campus_relevant": is_campus_relevant,
                "weight": weight
            }

    def _label_name(self, value: float) -> str:
        if value < 0:
            return "negative"
        elif value > 0:
            return "positive"
        return "neutral"

    def score_batch(self, payload: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        return [self.score_headline(item) for item in payload]

    def aggregate_score(self, scored_data: List[Dict[str, Any]]) -> float:
        """
        Returns a single sentiment score for the market using a weighted average.
        Range: -1.0 to +1.0
        """
        if not scored_data:
            return 0.0

        total_weight = sum(item.get("weight", 1.0) for item in scored_data)

        if total_weight == 0:
            return 0.0

        # Calculate weighted sum of sentiment
        weighted_sum = sum(item["sentiment"] * item.get("weight", 1.0) for item in scored_data)

        return float(weighted_sum / total_weight)


# --- PIPELINE ENTRY POINT ---

def run_nlp_scoring(news_payload: List[Dict[str, Any]]) -> Dict[str, Any]:
    scorer = ZeltaSentimentScorer()

    scored = scorer.score_batch(news_payload)
    aggregate = scorer.aggregate_score(scored)

    print(f"NLP Score (Market Sentiment): {aggregate:.3f}")

    return {
        "scored_headlines": scored,
        "aggregate_sentiment": round(aggregate, 3)
    }