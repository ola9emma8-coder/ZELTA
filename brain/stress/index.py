# stress/index.py

from typing import Dict

class ZeltaStressIndex:
    """
    Combines Bayse market signal + NLP sentiment -> Produces Stress Index (0-100)
    """

    def __init__(self, weight_sentiment: float = 0.4, weight_market: float = 0.6):
        # Increased market weight since Bayse is the PRIMARY signal
        self.weight_sentiment = weight_sentiment
        self.weight_market = weight_market

    def compute_market_prob(self, bayse_data: Dict) -> float:
        yes_price = bayse_data.get("yes_price", 50)
        return yes_price / 100.0

    def compute_sentiment_stress(self, sentiment: float) -> float:
        return abs(sentiment)

    def compute_market_stress(self, market_prob: float) -> float:
        return abs(market_prob - 0.5) * 2

    def combine(self, sentiment_stress: float, market_stress: float) -> float:
        return (sentiment_stress * self.weight_sentiment) + (market_stress * self.weight_market)

    def scale_to_100(self, value: float) -> int:
        return int(round(value * 100))

    def classify(self, stress_score: int) -> str:
        """Mapped strictly to ZELTA Framework Thresholds"""
        if stress_score <= 29:
            return "CALM"
        elif stress_score <= 59:
            return "MODERATE"
        elif stress_score <= 79:
            return "HIGH STRESS"
        else:
            return "CRISIS"

    def compute(self, bayse_data: Dict, sentiment_score: float) -> Dict:
        market_prob = self.compute_market_prob(bayse_data)
        sentiment_stress = self.compute_sentiment_stress(sentiment_score)
        market_stress = self.compute_market_stress(market_prob)

        combined = self.combine(sentiment_stress, market_stress)
        stress_score = self.scale_to_100(combined)

        return {
            "stress_score": stress_score,
            "level": self.classify(stress_score),
            "components": {
                "sentiment_stress": round(sentiment_stress, 3),
                "market_stress": round(market_stress, 3),
                "market_probability": round(market_prob, 3)
            }
        }

# --- PIPELINE ENTRY POINT ---
def run_stress_index(bayse_data: Dict, sentiment_score: float) -> Dict:
    engine = ZeltaStressIndex()
    result = engine.compute(bayse_data, sentiment_score)
    return result