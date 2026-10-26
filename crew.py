#combine the agents 
from crewai import Crew

from tasks.analyse_task import get_stock_analysis
from tasks.trade_task import trade_decision
from agents.trader_agent import trader_agent
from agents.analyst import analyst_agent

stock_crew=Crew(
    agents=[analyst_agent, trader_agent],
    tasks=[get_stock_analysis, trade_decision],
    verbose=True
)