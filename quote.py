import os
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")

def get_quote(symbol):
    url = "https://www.alphavantage.co/query"
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": symbol,
        "apikey": API_KEY
    }
    response = requests.get(url, params=params)
    data =  response.json()

    quote = data.get("Global Quote")
    if not quote:
        print(f"No data found for symbol: {symbol}. Full response: {data}")
        return None
    
    return{
        "symbol": quote["01. symbol"],
        "price": float(quote["05. price"]),
        "change": float(quote["09. change"]),
        "change_percent": quote["10. change percent"]
    }

    # print(data)

if __name__ == "__main__":
    result = get_quote("AAPL")   
    print(result)