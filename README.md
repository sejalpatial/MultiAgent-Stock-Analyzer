# StockIQ — AI-Powered Stock Analysis

StockIQ is an AI-powered stock research and analysis application built using CrewAI, Groq, Yahoo Finance, and Streamlit. It uses multiple AI agents to analyze stock market data and generate structured trading recommendations.

The application combines historical market information, price movements, trading volume, and volatility with AI-generated insights in an interactive dashboard.

## 🌐 Live Demo

**Try StockIQ here:** [Launch StockIQ AI Stock Analyzer](https://multiagent-stock-analyzer-jsp9sdggmrfmjtqudxmm8q.streamlit.app/)

Explore the interactive dashboard, view historical stock prices and trading volume, and generate AI-powered stock analysis reports.

## Features

- **AI Stock Analysis:** An Analyst agent evaluates available stock market data.
- **Trading Recommendations:** A Trader agent produces a Buy, Sell, or Hold recommendation based on the analysis.
- **Historical Market Data:** Retrieves daily stock prices and trading volume using Yahoo Finance.
- **Price Change Analysis:** Displays daily price changes and percentage movements.
- **Volatility Analysis:** Calculates historical daily and annualized volatility estimates.
- **Interactive Dashboard:** Visualizes stock information using Streamlit.
- **Historical Charts:** Displays closing-price and trading-volume charts.
- **Historical Data Table:** Shows open, high, low, close, and volume.
- **CSV Export:** Allows users to download historical market data.
- **AI Reports:** Displays the final report and individual agent outputs.

## Tech Stack

| Technology                 | Purpose                         |
| -------------------------- | ------------------------------- |
| Python                     | Core programming language       |
| CrewAI                     | Multi-agent orchestration       |
| Groq                       | Hosted LLM inference            |
| LiteLLM                    | LLM provider integration        |
| Yahoo Finance (`yfinance`) | Stock market data               |
| Streamlit                  | Interactive web dashboard       |
| Pandas                     | Data processing and analysis    |
| python-dotenv              | Environment variable management |

## Project Structure

```text
multi_agent_crew_ai/
│
├── agents/
│   ├── analyst.py
│   ├── trader_agent.py
│   └── groq_llm.py
│
├── tasks/
│   ├── analyse_task.py
│   └── trade_task.py
│
├── tools/
│   └── stock_research_tool.py
│
├── app.py
├── main.py
├── crew.py
├── requirements.txt
├── .gitignore
├── .env                  # Local secrets; not committed
└── README.md
```

##How It Works

1. The user enters a stock ticker, such as `TSLA`, `AAPL`, or `MSFT`.
2. The dashboard retrieves historical market data through Yahoo Finance.
3. The Analyst agent uses the stock research tool to examine the available data.
4. The Trader agent evaluates the analysis and produces a recommendation.
5. CrewAI orchestrates the tasks and returns their outputs.
6. Streamlit presents the market information, charts, and AI reports.

### Agent Architecture

**Financial Market Analyst**

- Retrieves stock information using the custom research tool.
- Examines available price movements, volume, and volatility.
- Summarizes market observations and potential risks.

**Strategic Stock Trader**

- Evaluates the Analyst's findings.
- Produces a Buy, Sell, or Hold recommendation.
- Explains the supporting evidence and risks.

The quality of the recommendation depends on the availability and accuracy of the underlying data.

## Prerequisites

- Python 3.11 recommended for this project setup
- Git
- A Groq API key
- Internet access for LLM requests and market-data retrieval

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
```

Replace the URL with your actual GitHub repository URL.

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
```

Use the exact environment variable expected by your Groq/LLM configuration. Never commit your `.env` file or expose your API key publicly.

### 5. Run the Streamlit dashboard

```bash
python -m streamlit run app.py
```

Open the local URL displayed in your terminal, usually:

http://localhost:8501

### Optional: Run the command-line entry point

```bash
python main.py
```

## Dashboard Overview

The dashboard provides:

- Latest available closing price
- Daily price change and percentage change
- Trading volume
- Historical volatility estimates
- Historical price chart
- Trading-volume chart
- Historical market-data table
- CSV download
- AI Analyst and Trader reports

Market data availability and timestamps depend on Yahoo Finance. The latest daily closing price may not represent the current live price.

## Deployment

StockIQ can be deployed using Streamlit Community Cloud.

1. Push the project to GitHub.
2. Visit https://share.streamlit.io/
3. Create a new application.
4. Select your repository and branch.
5. Set the main file path to `app.py`.
6. Configure the required API key in the application's Secrets settings.
7. Deploy and test the public URL.

Ensure that `.env`, `.venv/`, `venv/`, and Python cache files are excluded from Git.

## Security

- Keep API keys in environment variables or deployment secrets.
- Never upload `.env` or `.streamlit/secrets.toml`.
- Do not expose API keys in frontend code or screenshots.
- Review dependency versions and deployment logs if installation fails.

## Limitations

- Yahoo Finance data may be delayed, incomplete, or unavailable.
- Historical volatility describes past price variability and does not predict future performance.
- AI-generated recommendations may be inaccurate or insufficiently supported.
- Fundamental and macroeconomic analysis may be limited by the data currently available to the agents.
- The application does not execute trades through a brokerage account.
- Recommendations are not personalized financial advice.

## Future Improvements

- Add fundamental analysis using earnings, revenue, and financial ratios.
- Add technical indicators such as moving averages and RSI.
- Introduce explicit data-quality checks and an insufficient-data outcome.
- Add recommendation confidence calibration and historical backtesting.
- Save previous reports and compare recommendations over time.
- Improve report visualization with evidence summaries and risk indicators.
- Add a stock watchlist and multi-stock comparison.

## Disclaimer

StockIQ is an educational and research project. It is not a financial advisor, and its outputs should not be treated as guaranteed investment recommendations. Verify market information independently before making financial decisions.

## License

This project is available under the MIT License if you choose to distribute it under that license. Add a `LICENSE` file before claiming that the repository is MIT-licensed.
