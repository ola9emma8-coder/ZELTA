# api/routes.py

from fastapi import APIRouter
from typing import Dict, Any

# Import the updated LiveStressMonitor singleton
from brain.bayse.stress_signal import monitor

# Import the ZELTA intelligence pipeline components
from brain.stress.index import run_stress_index
from brain.bias.detector import run_bias_detection

router = APIRouter()


@router.get("/brain")
async def get_brain_data() -> Dict[str, Any]:
    """
    The main intelligence endpoint for ZELTA.
    Returns the live stress index number and the active behavioral bias
    using real-time WebSocket orderbook data from Bayse.
    """
    # 1. Fetch live Bayse crowd data from the background WebSocket monitor
    # The monitor continuously updates: {"score": 0.0, "status": "...", "price": 0.0, "spread": 0.0}
    live_signal = monitor.current_signal

    # Adapt the live mid-price (e.g., 0.50) to the 0-100 scale expected by the Stress Index pipeline
    # We default to 50 if it's still initializing
    bayse_data = {
        "yes_price": live_signal.get("price", 0.5) * 100
    }

    # 2. Fetch/Compute NLP Sentiment (Placeholder for now)
    # In a real app, this comes from an async background worker running the RoBERTa model
    current_sentiment_score = -0.45

    # 3. Compute the ZELTA Stress Index (0-100) using the live Bayse probability
    stress_result = run_stress_index(bayse_data, current_sentiment_score)

    # 4. Detect Active Behavioral Bias
    # Passing placeholder wallet context to satisfy the detector logic
    wallet_context = {"cash_withdrawal": True, "impulse_buy": False, "spending_spike": False}
    bias_result = run_bias_detection(stress_result, current_sentiment_score, wallet_data=wallet_context)

    return {
        "status": "success",
        "origin": "ZELTA Intelligence Layer",
        "data": {
            # Requested Core Outputs
            "stress_index": stress_result["stress_score"],
            "active_bias": bias_result["bias"],

            # Additional helpful context for the frontend
            "stress_level": stress_result["level"],  # e.g., "HIGH STRESS", "CRISIS"
            "bias_confidence": bias_result["confidence"],
            "explanation": bias_result["explanation"],

            # The raw WebSocket calculated state (micro-structure stress, spread, etc.)
            "bayse_ws_signal_raw": live_signal
        }
    }