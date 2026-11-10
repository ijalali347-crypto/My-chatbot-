import json

import anthropic

import config
import broker

client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)


def build_market_snapshot():
    return {
        "account": broker.get_account_summary(),
        "positions": broker.get_positions(),
        "allowed_symbols": config.ALLOWED_SYMBOLS,
        "max_order_value_usd": config.MAX_ORDER_VALUE_USD,
        "recent_daily_closes": {
            s: broker.get_recent_prices(s) for s in config.ALLOWED_SYMBOLS
        },
    }


def decide(snapshot):
    prompt = (
        config.STRATEGY_INSTRUCTION
        + "\n\nHere is the current data:\n"
        + json.dumps(snapshot, indent=2)
        + "\n\nReply with ONLY valid JSON in this exact shape:\n"
        + '{"decisions": [{"symbol": "AAPL", "action": "BUY|SELL|HOLD", '
        + '"dollars": 100, "reason": "short explanation"}]}'
    )

    response = client.messages.create(
        model=config.MODEL_NAME,
        max_tokens=1000,
        messages=[{"role": "user", "content": prompt}],
    )
    text = response.content[0].text.strip()
    if text.startswith("```"):
        text = text.strip("`").replace("json", "", 1).strip()
    return json.loads(text)
