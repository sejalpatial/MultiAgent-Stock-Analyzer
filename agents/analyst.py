#Defines the Financial Market Analyst and gives it the stock-data tool.
from crewai import Agent
from agents.groq_llm import GroqLLM

from tools.stock_research_tool import get_stock_price

#initialize the llm


llm = GroqLLM(
    model="groq/openai/gpt-oss-120b",
    temperature=0.0
)

analyst_agent= Agent(
    role="Financial Market Analyst",
     goal=(
        "Perform in-depth evaluations of publicly traded stocks using real-time data, "
        "identifying trends, performance insights, and key financial signals to support decision-making."
    ),
    backstory=(
        "You are a veteran financial analyst with deep expertise in interpreting stock market data, "
        "technical trends, and fundamentals. You specialize in producing well-structured reports that evaluate "
        "stock performance using live market indicators."
    ),
    llm=llm,
    tools=[get_stock_price],
    verbose=True   #you can see intermediate steps
)

