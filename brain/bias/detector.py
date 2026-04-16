# bias/detector.py

from typing import Dict, Optional


class ZeltaBiasDetector:
    """
    Identifies active bias from stress index + wallet patterns:
    loss aversion, present bias, overconfidence, herd behavior, mental accounting.
    """

    def detect(self, stress_data: Dict, sentiment_score: float, wallet_data: Optional[Dict] = None) -> Dict:
        stress_score = stress_data.get("stress_score", 50)
        market_prob = stress_data["components"].get("market_probability", 0.5)

        # Default wallet metrics if not provided
        if not wallet_data:
            wallet_data = {"spending_spike": False, "cash_withdrawal": False, "impulse_buy": False}

        bias = "Neutral"
        confidence = "Low"
        explanation = ""

        # 1. Loss Aversion: High stress + negative sentiment + cash hoarding/withdrawal
        if stress_score >= 60 and wallet_data.get("cash_withdrawal"):
            bias = "Loss Aversion"
            confidence = "High"
            explanation = "Market fear is high. You are exhibiting cash hoarding behavior driven by panic."

        # 2. Present Bias: Impulse buying despite upcoming obligations
        elif wallet_data.get("impulse_buy"):
            bias = "Present Bias"
            confidence = "High"
            explanation = "You are prioritizing immediate gratification over impending financial obligations."

        # 3. Overconfidence: Low stress + high positive sentiment + risky allocation
        elif stress_score < 30 and sentiment_score > 0.3:
            bias = "Overconfidence"
            confidence = "Medium"
            explanation = "Market is overly optimistic. Overconfidence risk is active."

        # 4. Herd Behavior: Moderate/High stress + following extreme market probabilities
        elif 40 <= stress_score < 70 and abs(market_prob - 0.5) > 0.35:
            bias = "Herd Behavior"
            confidence = "Medium"
            explanation = "Market positioning is highly one-sided. You may be following the crowd without analysis."

        # 5. Mental Accounting (Fallback if unusual categorization detected)
        elif wallet_data.get("spending_spike") and stress_score < 60:
            bias = "Mental Accounting"
            confidence = "Low"
            explanation = "Spending is elevated. Ensure you are viewing your finances as a unified whole."

        # Rational / Calm
        elif stress_score < 30:
            bias = "Rational"
            confidence = "Low"
            explanation = "Market appears stable. Decisions are likely logical."

        return {
            "bias": bias,
            "confidence": confidence,
            "explanation": explanation,
            "inputs": {
                "stress_score": stress_score,
                "sentiment": sentiment_score,
                "market_probability": market_prob
            }
        }


# --- PIPELINE ENTRY POINT ---
def run_bias_detection(stress_data: Dict, sentiment_score: float, wallet_data: Dict = None) -> Dict:
    detector = ZeltaBiasDetector()
    result = detector.detect(stress_data, sentiment_score, wallet_data)
    return result