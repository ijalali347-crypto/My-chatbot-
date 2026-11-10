import json
import os
import time
import traceback
from datetime import datetime

import config
import broker
import agent

os.makedirs("logs", exist_ok=True)
LOG_FILE = "logs/decisions.jsonl"


def log(entry):
    entry["time"] = datetime.now().isoformat()
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


def run_once():
    snapshot = agent.build_market_snapshot()
    decision = agent.decide(snapshot)

    for d in decision.get("decisions", []):
        symbol = d.get("symbol")
        action = str(d.get("action", "HOLD")).upper()
        dollars = float(d.get("dollars", 0) or 0)
        reason = d.get("reason", "")

        if action in ("BUY", "SELL") and dollars > 0:
            result = broker.place_order(symbol, action.lower(), dollars)
        else:
            result = "HOLD - no order"

        print(f"{symbol}: {action} {dollars} -> {result}")
        log(
            {
                "symbol": symbol,
                "action": action,
                "dollars": dollars,
                "reason": reason,
                "result": result,
                "equity": snapshot["account"]["equity"],
            }
        )


if __name__ == "__main__":
    print("AI paper trading agent started. Press Ctrl+C to stop.")
    while True:
        try:
            run_once()
        except Exception:
            traceback.print_exc()
            log({"error": traceback.format_exc()})
        time.sleep(config.LOOP_INTERVAL_SECONDS)
