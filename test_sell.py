from portfolio import load_portfolio, save_portfolio, sell_stock

portfolio = load_portfolio()

success, message = sell_stock(portfolio, "AAPL", 5, 280.00)
print(message)

save_portfolio(portfolio)
print(portfolio)