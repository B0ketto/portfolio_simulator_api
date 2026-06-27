from fastapi import FastAPI
from pydantic import BaseModel
from quote import get_quote
from portfolio import load_portfolio, save_portfolio, buy_stock, sell_stock

app = FastAPI(title="Portfolio Simulator API")

class TradeRequest(BaseModel):
    symbol: str
    shares: int

@app.get("/")
def root():
    return {"message": "Portfolio Simulator API is running"}

@app.get("/portfolio")
def get_portfolio():
    portfolio = load_portfolio()
    return portfolio

@app.post("/buy")
def buy(trade: TradeRequest):
    portfolio = load_portfolio()
    quote = get_quote(trade.symbol)
    if not quote:
        return {"success": False, "message": f"Couldn't fetch price for {trade.symbol}"}

    success, message = buy_stock(portfolio, trade.symbol, trade.shares, quote["price"])
    save_portfolio(portfolio)
    return {"success": success, "message": message}

@app.post("/sell")
def sell(trade: TradeRequest):
    portfolio = load_portfolio()
    quote = get_quote(trade.symbol)
    if not quote:
        return {"success": False, "message": f"Couldn't fetch price for {trade.symbol}"}

    success, message = sell_stock(portfolio, trade.symbol, trade.shares, quote["price"])
    save_portfolio(portfolio)
    return {"success": success, "message": message}