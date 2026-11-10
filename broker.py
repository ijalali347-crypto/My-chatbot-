from datetime import datetime, timedelta

from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest
from alpaca.data.timeframe import TimeFrame

import config

trading_client = TradingClient(
    config.ALPACA_API_KEY, config.ALPACA_SECRET_KEY, paper=config.PAPER
)
data_client = StockHistoricalDataClient(
    config.ALPACA_API_KEY, config.ALPACA_SECRET_KEY
)

orders_today = {"date": None, "count": 0}


def get_account_summary():
    acct = trading_client.get_account()
    return {
        "cash": float(acct.cash),
        "equity": float(acct.equity),
        "buying_power": float(acct.buying_power),
    }


def get_positions():
    positions = trading_client.get_all_positions()
    return {
        p.symbol: {
            "qty": float(p.qty),
            "avg_entry": float(p.avg_entry_price),
            "unrealized_pl": float(p.unrealized_pl),
        }
        for p in positions
    }


def get_recent_prices(symbol, days=30):
    request = StockBarsRequest(
        symbol_or_symbols=symbol,
        timeframe=TimeFrame.Day,
        start=datetime.now() - timedelta(days=days + 10),
    )
    bars = data_client.get_stock_bars(request).df
    closes = bars["close"].tolist()[-days:]
    return [round(c, 2) for c in closes]


def place_order(symbol, side, dollars):
    """Place a paper market order, after checking every safety limit."""
    today = datetime.now().date()
    if orders_today["date"] != today:
        orders_today["date"] = today
        orders_today["count"] = 0

    if symbol not in config.ALLOWED_SYMBOLS:
        return f"BLOCKED: {symbol} is not in the allowed list."
    if dollars > config.MAX_ORDER_VALUE_USD:
        return f"BLOCKED: order {dollars} is above the max {config.MAX_ORDER_VALUE_USD}."
    if orders_today["count"] >= config.MAX_DAILY_ORDERS:
        return "BLOCKED: daily order limit reached."

    positions = get_positions()
    if (
        side == "buy"
        and symbol not in positions
        and len(positions) >= config.MAX_OPEN_POSITIONS
    ):
        return "BLOCKED: too many open positions."
    if side == "sell" and symbol not in positions:
        return f"BLOCKED: you do not hold {symbol}."

    order = MarketOrderRequest(
        symbol=symbol,
        notional=round(dollars, 2),
        side=OrderSide.BUY if side == "buy" else OrderSide.SELL,
        time_in_force=TimeInForce.DAY,
    )
    result = trading_client.submit_order(order)
    orders_today["count"] += 1
    return f"ORDER PLACED: {side} {dollars} of {symbol} (id {result.id})"
