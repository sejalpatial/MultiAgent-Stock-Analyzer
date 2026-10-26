
from crewai import Task
from agents.trader_agent import trader_agent
from tasks.analyse_task import get_stock_analysis

trade_decision = Task(
    description=(
        "Evaluate {stock} using the market data and findings in the "
        "analyst's preceding report. Consider daily price change, trading "
        "volume, historical price movement, volatility, and data limitations. "
        "Choose Buy, Sell, or Hold as an educational research conclusion. "
        "Explain the evidence and major risks. If the report lacks enough "
        "evidence, explicitly say so instead of inventing indicators. "
        "Do not promise returns or present the result as personalized "
        "financial advice."
    ),
    expected_output=(
    "Return the report using exactly this structure. "
    "Put the recommendation on the first line.\n\n"
    "RECOMMENDATION: BUY, SELL, or HOLD\n"
    "CONFIDENCE: Low, Moderate, or High\n"
    "RISK LEVEL: Low, Moderate, or High\n\n"
    "SUMMARY:\n"
    "Explain the decision in 2-3 concise sentences.\n\n"
    "KEY EVIDENCE:\n"
    "- Give 2-4 bullet points based on the analyst's actual data.\n\n"
    "RISKS:\n"
    "- Give 1-3 important risks or limitations.\n\n"
    "WHAT COULD CHANGE THIS DECISION:\n"
    "- Explain what additional evidence could change the conclusion.\n\n"
    "Do not invent data, guarantee returns, or provide personalized "
    "financial advice. If evidence is insufficient, say so clearly. "
    "Confidence and risk are qualitative agent assessments, not "
    "statistical predictions."
),
    agent=trader_agent,
    context=[get_stock_analysis],
)
