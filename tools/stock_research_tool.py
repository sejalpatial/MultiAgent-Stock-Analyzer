import yfinance as yf  #Python library that lets you retrieve stock market data from Yahoo Finance using Python code.
from crewai.tools import tool #imports the tool decorator, which can turn a Python function into a tool that an agent can use.

@tool("Live Stock INformation Tool")
def get_stock_price(stock_symbol: str) -> str:
     """
    Retrieves the latest stock price and other relevant info
    for a given stock symbol using Yahoo Finance.

    Parameters:
        stock_symbol (str): The ticker symbol of the stock
        (e.g., AAPL, TSLA, MSFT).

    Returns:
        str: A summary of the stock's current price,
        daily change, and other key data.
    """

     stock=yf.Ticker(stock_symbol) #creates an object representing a particular stock
     info=stock.info #extracts the available info of the stock symbol using yfinance and returns a dictionary

     current_price=info.get("regularMarketPrice")
     change=info.get("regularMarketChange")
     changePercent=info.get("regularMarketChangePercent")
     currency=info.get("currency","USD")

     if current_price is None:
          return f" Could not return price for {stock_symbol} . Please check the symbol again"

     return(
          f"Stock {stock_symbol.upper()}\n"
          f"Price {current_price} {currency}\n"
          f"Change {change} ({round(changePercent,2)}%)"
     )

#print(get_stock_price("AAPL"))
