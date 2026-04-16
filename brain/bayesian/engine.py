# bayesian/engine.py

from typing import Dict
import scipy.stats as stats # Matches architecture spec

class ZeltaBayesianEngine:
    """
    Adjusts market probability using formal Bayesian inference.
    Posterior Odds = Prior Odds * Likelihood Ratio (derived from bias/stress).
    """

    def __init__(self, base_rate_prior: float = 0.5):
        """
        base_rate_prior = Historical probability before current panic (Bayse base rate)
        """
        self.base_rate_prior = base_rate_prior

    def compute_likelihood_ratio(self, bias: str, stress_score: int) -> float:
        """
        Determine how much the current bias is distorting the crowd's signal.
        LR > 1 amplifies the prior (validates), LR < 1 discounts the crowd's panic.
        """
        stress_factor = stress_score / 100.0

        # Loss Aversion/Panic -> Crowd is overestimating risk -> Discount the evidence
        if bias in ["Loss Aversion", "Panic Selling"]:
            return max(0.2, 1.0 - (0.8 * stress_factor))

        # Overconfidence/Present Bias -> Crowd is underestimating risk -> Inflate the evidence
        elif bias in ["Overconfidence", "Present Bias"]:
            return min(3.0, 1.0 + (2.0 * stress_factor))

        # Herd Behavior -> Mild discounting due to unverified momentum
        elif bias == "Herd Behavior":
            return max(0.5, 1.0 - (0.4 * stress_factor))

        # Rational/Calm -> Trust the crowd (LR = 1.0)
        return 1.0

    def adjust_probability(
        self,
        market_prob: float,
        bias: str,
        stress_score: int
    ) -> float:
        """
        Bayesian update: convert to odds, apply likelihood ratio, convert back.
        """
        # 1. Convert Bayse Crowd Probability to Odds
        # Avoid division by zero
        market_prob = max(0.01, min(0.99, market_prob))
        prior_odds = market_prob / (1.0 - market_prob)

        # 2. Calculate Likelihood Ratio based on behavioral distortion
        lr = self.compute_likelihood_ratio(bias, stress_score)

        # 3. Calculate Posterior Odds
        posterior_odds = prior_odds * lr

        # 4. Convert back to Rational Probability (Posterior)
        rational_prob = posterior_odds / (1.0 + posterior_odds)

        return rational_prob

    def compute_edge(self, market_prob: float, rational_prob: float) -> float:
        """
        Edge = Confidence in outcome (difference between rational belief and market belief)
        """
        return rational_prob - market_prob

    def confidence_level(self, edge: float) -> str:
        abs_edge = abs(edge)
        if abs_edge < 0.05:
            return "Low"
        elif abs_edge < 0.15:
            return "Medium"
        else:
            return "High"

    def decide(self, edge: float, rational_prob: float) -> str:
        """
        Outputs exact verdict string
        """
        if rational_prob > 0.55 and edge > 0.05:
            return "INVEST"
        elif rational_prob < 0.45 and edge < -0.05:
            return "SAVE"
        else:
            return "HOLD"

    def run(self, stress_data: Dict, bias_data: Dict) -> Dict:
        market_prob = stress_data["components"]["market_probability"]
        stress_score = stress_data["stress_score"]
        bias = bias_data["bias"]

        rational_prob = self.adjust_probability(market_prob, bias, stress_score)
        edge = self.compute_edge(market_prob, rational_prob)

        return {
            "market_probability": round(market_prob, 3),
            "rational_probability": round(rational_prob, 3),
            "edge": round(edge, 3),
            "confidence": self.confidence_level(edge),
            "decision": self.decide(edge, rational_prob)
        }

# --- PIPELINE ENTRY POINT ---
def run_bayesian_engine(stress_data: Dict, bias_data: Dict) -> Dict:
    engine = ZeltaBayesianEngine()
    result = engine.run(stress_data, bias_data)
    return result