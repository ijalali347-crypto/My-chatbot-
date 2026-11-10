# AI Paper Trading Agent

Paper-trading bot using an Alpaca demo account and an AI model.
Paper trading only: no real money.

## Setup

1. Copy `.env.example` to `.env` and fill in your keys. Never upload `.env`.
2. `pip install -r requirements.txt`
3. `python main.py`

Every decision is saved in `logs/decisions.jsonl`.
Change symbols, limits and the strategy instruction in `config.py`.

Not financial advice. Learning project only.
