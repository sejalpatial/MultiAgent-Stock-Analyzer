#Defines the Strategic Stock Trader.
from crewai import Agent
from agents.groq_llm import GroqLLM


llm=GroqLLM(
    model="groq/openai/gpt-oss-120b",
    temperature =0

)
trader_agent=Agent(
    role="Strategic Stock Trader",
    goal=(
        "decide whether to buy , sell or hold a given stock based on live market data," \
        "price movements , and financial analysis with the available data ."

    ),
    backstory=(
        "You are a strategic trader with years of experience in timing market entry and exit points" \
        "You rely on real-time stock data , daily price movements , and volume trends to make trading decisions" \
        "that optimize returns and reduce risks"
    ),
    llm=llm,
    tools=[],
    verbose=True
)