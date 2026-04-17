from typing import Dict

class QueloConfidenceScorer:
    """
    Evaluates the overall reliability of a QUELO verdict.
    
    While the Bayesian Engine calculates the mathematical edge, this module 
    determines how much we actually *trust* that edge before sending it to 
    the Kelly Allocator.
    """

    def __init__(self):
        # Base score starts at 50 (neutral)
        self.BASE_SCORE = 50

    def evaluate_edge_strength(self, edge: float) -> int:
        """Scores the mathematical edge (0 to +30 points)."""
        abs_edge = abs(edge)
        if abs_edge >= 0.20:
            return 30
        elif abs_edge >= 0.10:
            return 20
        elif abs_edge >= 0.05:
            return 10
        return 0

    def evaluate_market_stress(self, stress_score: int) -> int:
        """Penalizes confidence if the market is too chaotic (0 to -40 points)."""
        if stress_score >= 80:
            return -40  # Extreme crisis, high uncertainty
        elif stress_score >= 60:
            return -20  # Elevated stress, moderate uncertainty
        elif stress_score <= 30:
            return 10   # Calm market, higher predictability
        return 0

    def evaluate_conviction(self, rational_prob: float) -> int:
        """Scores how definitive the model's belief is (0 to +20 points)."""
        # If the probability is closer to 0% or 100%, conviction is higher.
        # If it's near 50%, it's essentially a coin toss.
        distance_from_center = abs(0.5 - rational_prob)
        
        if distance_from_center >= 0.30: # e.g., > 80% or < 20%
            return 20
        elif distance_from_center >= 0.15: # e.g., > 65% or < 35%
            return 10
        return 0

    def get_confidence_label(self, total_score: int) -> str:
        if total_score >= 80:
            return "Very High"
        elif total_score >= 60:
            return "High"
        elif total_score >= 40:
            return "Medium"
        else:
            return "Low"

    def run(self, bayesian_data: Dict, stress_data: Dict) -> Dict:
        """
        Main entry point called by brain/pipeline.py
        
        Args:
            bayesian_data: Output from QueloBayesianEngine
            stress_data: Output from stress/index.py
        """
        edge = bayesian_data.get("edge", 0.0)
        rational_prob = bayesian_data.get("rational_probability", 0.5)
        stress_score = stress_data.get("score", 50)
        verdict = bayesian_data.get("verdict", "HOLD")

        # 1. Calculate Score Components
        edge_points = self.evaluate_edge_strength(edge)
        stress_points = self.evaluate_market_stress(stress_score)
        conviction_points = self.evaluate_conviction(rational_prob)

        # 2. Tally Total Score (Capped between 0 and 100)
        raw_score = self.BASE_SCORE + edge_points + stress_points + conviction_points
        final_score = max(0, min(100, raw_score))

        # 3. Force Low Confidence on HOLD verdicts
        if verdict == "HOLD":
            final_score = min(final_score, 39) # Force into "Low" tier

        label = self.get_confidence_label(final_score)

        return {
            "confidence_score_100": final_score,
            "confidence_tier": label,
            "metrics": {
                "edge_contribution": edge_points,
                "stress_penalty": stress_points,
                "conviction_contribution": conviction_points
            },
            "is_actionable": final_score >= 60 # Boolean flag for the Allocator
        }

# ── PIPELINE ENTRY POINT ──────────────────────────────────────────────────────

def run_confidence_scorer(bayesian_data: Dict, stress_data: Dict) -> Dict:
    """Called by brain/pipeline.py right after the Bayesian Engine"""
    scorer = QueloConfidenceScorer()
    result = scorer.run(bayesian_data, stress_data)
    
    print(
        f"[QUELO Confidence] Score: {result['confidence_score_100']}/100 "
        f"| Tier: {result['confidence_tier']} "
        f"| Actionable: {result['is_actionable']}"
    )
    return resultfrom typing import Dict

class QueloConfidenceScorer:
    """
    Evaluates the overall reliability of a QUELO verdict.
    
    While the Bayesian Engine calculates the mathematical edge, this module 
    determines how much we actually *trust* that edge before sending it to 
    the Kelly Allocator.
    """

    def __init__(self):
        # Base score starts at 50 (neutral)
        self.BASE_SCORE = 50

    def evaluate_edge_strength(self, edge: float) -> int:
        """Scores the mathematical edge (0 to +30 points)."""
        abs_edge = abs(edge)
        if abs_edge >= 0.20:
            return 30
        elif abs_edge >= 0.10:
            return 20
        elif abs_edge >= 0.05:
            return 10
        return 0

    def evaluate_market_stress(self, stress_score: int) -> int:
        """Penalizes confidence if the market is too chaotic (0 to -40 points)."""
        if stress_score >= 80:
            return -40  # Extreme crisis, high uncertainty
        elif stress_score >= 60:
            return -20  # Elevated stress, moderate uncertainty
        elif stress_score <= 30:
            return 10   # Calm market, higher predictability
        return 0

    def evaluate_conviction(self, rational_prob: float) -> int:
        """Scores how definitive the model's belief is (0 to +20 points)."""
        # If the probability is closer to 0% or 100%, conviction is higher.
        # If it's near 50%, it's essentially a coin toss.
        distance_from_center = abs(0.5 - rational_prob)
        
        if distance_from_center >= 0.30: # e.g., > 80% or < 20%
            return 20
        elif distance_from_center >= 0.15: # e.g., > 65% or < 35%
            return 10
        return 0

    def get_confidence_label(self, total_score: int) -> str:
        if total_score >= 80:
            return "Very High"
        elif total_score >= 60:
            return "High"
        elif total_score >= 40:
            return "Medium"
        else:
            return "Low"

    def run(self, bayesian_data: Dict, stress_data: Dict) -> Dict:
        """
        Main entry point called by brain/pipeline.py
        
        Args:
            bayesian_data: Output from QueloBayesianEngine
            stress_data: Output from stress/index.py
        """
        edge = bayesian_data.get("edge", 0.0)
        rational_prob = bayesian_data.get("rational_probability", 0.5)
        stress_score = stress_data.get("score", 50)
        verdict = bayesian_data.get("verdict", "HOLD")

        # 1. Calculate Score Components
        edge_points = self.evaluate_edge_strength(edge)
        stress_points = self.evaluate_market_stress(stress_score)
        conviction_points = self.evaluate_conviction(rational_prob)

        # 2. Tally Total Score (Capped between 0 and 100)
        raw_score = self.BASE_SCORE + edge_points + stress_points + conviction_points
        final_score = max(0, min(100, raw_score))

        # 3. Force Low Confidence on HOLD verdicts
        if verdict == "HOLD":
            final_score = min(final_score, 39) # Force into "Low" tier

        label = self.get_confidence_label(final_score)

        return {
            "confidence_score_100": final_score,
            "confidence_tier": label,
            "metrics": {
                "edge_contribution": edge_points,
                "stress_penalty": stress_points,
                "conviction_contribution": conviction_points
            },
            "is_actionable": final_score >= 60 # Boolean flag for the Allocator
        }

# ── PIPELINE ENTRY POINT ──────────────────────────────────────────────────────

def run_confidence_scorer(bayesian_data: Dict, stress_data: Dict) -> Dict:
    """Called by brain/pipeline.py right after the Bayesian Engine"""
    scorer = QueloConfidenceScorer()
    result = scorer.run(bayesian_data, stress_data)
    
    print(
        f"[QUELO Confidence] Score: {result['confidence_score_100']}/100 "
        f"| Tier: {result['confidence_tier']} "
        f"| Actionable: {result['is_actionable']}"
    )
    return result
