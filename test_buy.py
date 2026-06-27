from portfolio import load_portfolio, save_portfolio, buy_stock

portfolio = load_portfolio()

success, message = buy_stock(portfolio, "AAPL", 10, 275.15)
print(message)

save_portfolio(portfolio)
print(portfolio)