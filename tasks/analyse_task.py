
from crewai import Task
from agents.analyst import analyst_agent

get_stock_analysis = Task(
    description=(
        "Analyze the stock {stock} using the Live Stock Information Tool. "
        "Retrieve the latest available closing price, daily price change, "
        "percentage change, trading volume, period high and low, historical "
        "closing prices, and historical volatility. "
        "Use only the data actually returned by the tool. "
        "Clearly state the latest available trading date. "
        "Explain recent price movements and volume observations. "
        "Do not invent missing values or claim that historical data is "
        "a real-time quote. Provide balanced risks and limitations."
    ),
    expected_output=(
        "A structured stock analysis containing:\n"
        "1. Latest available closing price and date\n"
        "2. Daily price change and percentage\n"
        "3. Latest trading session volume\n"
        "4. Period high and low\n"
        "5. Historical prices and volume observations\n"
        "6. Daily and annualized historical volatility, if available\n"
        "7. Key observations, risks, and limitations\n"
        "8. A cautious summary, without guaranteeing investment returns"
    ),
    agent=analyst_agent,
)
