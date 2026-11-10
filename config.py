import os
from dotenv import load_dotenv

load_dotenv()

ALPACA_API_KEY = os.getenv("ALPACA_API_KEY")
ALPACA_SECRET_KEY = os.getenv("ALPACA_SECRET_KEY")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")

# Paper trading only. Keep this True.
PAPER = True

# Which symbols the agent is allowed to trade
ALLOWED_SYMBOLS = ["AAPL", "MSFT", "SPY"]

# Hard risk limits (enforced in code, not by the AI)
MAX_ORDER_VALUE_USD = 500       # max dollars per single order
MAX_OPEN_POSITIONS = 3          # max different stocks held at once
MAX_DAILY_ORDERS = 5            # max orders per day

# How often the agent runs, in seconds
LOOP_INTERVAL_SECONDS = 900     # every 15 minutes

# AI model name
MODEL_NAME = "claude-sonnet-5-5"

# Your instruction to the agent. Edit this to change its behaviour.
STRATEGY_INSTRUCTION = """
You are a cautious paper-trading agent.
Goal: grow the paper account slowly while avoiding large losses.
Rules:
- Only trade the allowed symbols.
- Prefer small positions.
- Only buy when the recent trend is clearly upward.
- Sell or avoid when the trend is clearly downward.
- If unsure, choose HOLD.
- Always explain your reasoning in one or two sentences.
"""
