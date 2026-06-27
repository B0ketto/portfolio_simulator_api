import json
import os
from datetime import datetime

PORTFOLIO_FILE = "portfolio.json"
STARTING_CASH = 10000.0

def load_portfolio():
    """Load portfolio from disk, or create a fresh one if it doesn't exist."""
    if not os.path.exists(PORTFOLIO_FILE):
        return {
            "cash": STARTING_CASH,
            "holdings": {},  
            "transactions": []
        }
    with open(PORTFOLIO_FILE, "r") as f:
        return json.load(f)

def save_portfolio(portfolio):
    """Save portfolio to disk."""
    with open(PORTFOLIO_FILE, "w") as f:
        json.dump(portfolio, f, indent=2)

def log_transaction(portfolio, action, symbol, shares, price):
    """Record a buy/sell event in the transaction history."""
    portfolio["transactions"].append({
        "timestamp": datetime.now().isoformat(),
        "action": action,        # "BUY" or "SELL"
        "symbol": symbol,
        "shares": shares,
        "price": price,
        "total_value": round(shares * price, 2)
    })

def buy_stock(portfolio, symbol, shares, price):
    """Buy shares of a stock at the given price. Returns (success, message)."""
    cost = shares * price

    if cost > portfolio["cash"]:
        return False, f"Not enough cash. Need ${cost:.2f}, have ${portfolio['cash']:.2f}"

    # Deduct cash
    portfolio["cash"] -= cost

    # Update holdings
    if symbol in portfolio["holdings"]:
        existing = portfolio["holdings"][symbol]
        total_shares = existing["shares"] + shares
        # weighted average price across old + new shares
        total_cost = (existing["shares"] * existing["avg_price"]) + cost
        new_avg_price = total_cost / total_shares

        portfolio["holdings"][symbol] = {
            "shares": total_shares,
            "avg_price": round(new_avg_price, 2)
        }
    else:
        portfolio["holdings"][symbol] = {
            "shares": shares,
            "avg_price": price
        }

    log_transaction(portfolio, "BUY", symbol, shares, price)
    return True, f"Bought {shares} shares of {symbol} at ${price:.2f}"


def sell_stock(portfolio, symbol, shares, price):
    """Sell shares of a stock at the given price. Returns (success, message)."""
    if symbol not in portfolio["holdings"]:
        return False, f"You don't own any {symbol}"

    holding = portfolio["holdings"][symbol]

    if shares > holding["shares"]:
        return False, f"You only own {holding['shares']} shares of {symbol}, can't sell {shares}"

    # Calculate profit/loss on the shares being sold
    cost_basis = holding["avg_price"] * shares
    proceeds = price * shares
    profit_loss = proceeds - cost_basis

    # Update cash
    portfolio["cash"] += proceeds

    # Update or remove holding
    remaining_shares = holding["shares"] - shares
    if remaining_shares == 0:
        del portfolio["holdings"][symbol]
    else:
        portfolio["holdings"][symbol]["shares"] = remaining_shares
        # avg_price stays the same — selling doesn't change your cost basis on remaining shares

    log_transaction(portfolio, "SELL", symbol, shares, price)
    return True, f"Sold {shares} shares of {symbol} at ${price:.2f} (P&L: ${profit_loss:+.2f})"