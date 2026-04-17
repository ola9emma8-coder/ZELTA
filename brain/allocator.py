from typing import Dict

class QueloKellyAllocator:
    """
    Determines exactly how much capital to deploy based on the mathematical
    edge and the system's confidence level.
    """

    def __init__(self):
        # Using "Half-Kelly" is a standard safety measure in quant finance
        self.KELLY_MULTIPLIER = 0.50 
        
        # Never allocate more than this % of total portfolio to a single move
        self.MAX_ALLOCATION_PCT = 0.15 
        
        # Default reward-to-risk ratio (Assumes we make $1.50 for every $1 risked)
        self.DEFAULT_PAYOFF_RATIO = 1.5 

    def calculate_base_kelly(self, win_probability: float, payoff_ratio: float) -> float:
        """
        The classic Kelly Criterion formula.
        Returns the raw percentage of capital to allocate (0.0 to 1.0).
        """
        loss_probability = 1.0 - win_probability
        
        # f* = p - (q / b)
        kelly_pct = win_probability - (loss_probability / payoff_ratio)
        
        # If edge is negative, Kelly will be negative. Floor it to 0.
        return max(0.0, kelly_pct)

    def scale_by_confidence(self, base_allocation: float, confidence_score: int) -> float:
        """
        Reduces the bet size if the system's confidence is low.
        A score of 100 keeps the full bet. A score of 60 cuts it down.
        """
        confidence_multiplier = confidence_score / 100.0
        return base_allocation * confidence_multiplier

    def run(self, bayesian_data: Dict, confidence_data: Dict, portfolio_balance: float) -> Dict:
        """
        Main entry point called by brain/pipeline.py.
        """
        verdict = bayesian_data.get("verdict", "HOLD")
        win_prob = bayesian_data.get("win_probability", 0.0)
        is_actionable = confidence_data.get("is_actionable", False)
        confidence_score = confidence_data.get("confidence_score_100", 0)

        # 1. The Hard Stops (Protect the Capital)
        if verdict == "HOLD" or not is_actionable:
            return self._build_response("HOLD", 0.0, 0.0, "System constraint: Not actionable or HOLD verdict.")

        # 2. Calculate Raw Kelly
        # (If verdict is SAVE, we are calculating how much capital to move to safety)
        base_kelly = self.calculate_base_kelly(win_prob, self.DEFAULT_PAYOFF_RATIO)

        # 3. Apply Safety Dampeners (Half-Kelly)
        fractional_kelly = base_kelly * self.KELLY_MULTIPLIER

        # 4. Scale by System Confidence
        adjusted_kelly = self.scale_by_confidence(fractional_kelly, confidence_score)

        # 5. Apply Absolute Maximum Caps
        final_allocation_pct = min(adjusted_kelly, self.MAX_ALLOCATION_PCT)
        
        # Calculate actual dollar amount
        dollar_amount = round(portfolio_balance * final_allocation_pct, 2)
        
        # Format percentage for display
        display_pct = round(final_allocation_pct * 100, 2)

        reasoning = (
            f"Base Kelly suggested {round(base_kelly*100, 1)}%. "
            f"Reduced to {display_pct}% due to safety parameters "
            f"and a confidence score of {confidence_score}/100."
        )

        return self._build_response(verdict, final_allocation_pct, dollar_amount, reasoning)

    def _build_response(self, action: str, percentage: float, amount: float, notes: str) -> Dict:
        return {
            "recommended_action": action,     # INVEST, SAVE, or HOLD
            "allocation_percentage": percentage,
            "allocation_amount": amount,
            "allocator_notes": notes
        }

# ── PIPELINE ENTRY POINT ──────────────────────────────────────────────────────

def run_kelly_allocator(bayesian_data: Dict, confidence_data: Dict, portfolio_balance: float) -> Dict:
    """Called by brain/pipeline.py right after Confidence Scorer"""
    allocator = QueloKellyAllocator()
    result = allocator.run(bayesian_data, confidence_data, portfolio_balance)
    
    print(
        f"[QUELO Kelly] Action: {result['recommended_action']} "
        f"| Amount: ${result['allocation_amount']} "
        f"({round(result['allocation_percentage']*100, 2)}%)"
    )
    return result
