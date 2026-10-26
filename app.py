
import streamlit as st
import yfinance as yf
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

from crew import stock_crew


# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="StockIQ | AI Market Intelligence",
    page_icon="📈",
    layout="wide",
)

# ---------------- STYLING ----------------
st.markdown("""
<style>
    .stApp {
        background-color: #0b1120;
        color: #f1f5f9;
    }

    [data-testid="stSidebar"] {
        background-color: #111827;
    }

    [data-testid="stMetric"] {
        background-color: #172033;
        border: 1px solid #273449;
        padding: 16px;
        border-radius: 12px;
    }

    .subtitle {
        color: #94a3b8;
        font-size: 15px;
    }
</style>
""", unsafe_allow_html=True)


# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.title("📈 StockIQ")
    st.caption("AI Market Intelligence")

    stock_symbol = st.text_input(
        "Stock ticker",
        value="TSLA",
        placeholder="e.g. TSLA, AAPL, MSFT",
    ).strip().upper()

    analyze_button = st.button(
        "🚀 Run AI Analysis",
        type="primary",
        use_container_width=True,
    )

    st.divider()
    st.subheader("Quick Select")

    quick_stocks = {
        "Tesla": "TSLA",
        "Apple": "AAPL",
        "Microsoft": "MSFT",
        "NVIDIA": "NVDA",
        "Amazon": "AMZN",
    }

    for company, symbol in quick_stocks.items():
        if st.button(company, key=f"quick_{symbol}",
                     use_container_width=True):
            st.session_state["selected_stock"] = symbol
            st.rerun()

if "selected_stock" in st.session_state:
    stock_symbol = st.session_state.pop("selected_stock")


# ---------------- MARKET DATA ----------------
@st.cache_data(ttl=300, show_spinner=False)
def get_market_data(symbol):
    ticker = yf.Ticker(symbol)
    history = ticker.history(period="1mo", interval="1d")

    if history.empty:
        raise ValueError(
            "No market data found. Check the ticker symbol."
        )

    history = history.dropna(subset=["Close"])

    if history.empty:
        raise ValueError("No valid closing prices are available.")

    closes = history["Close"]
    latest = history.iloc[-1]

    latest_close = float(latest["Close"])
    latest_volume = int(latest["Volume"])

    previous_close = (
        float(closes.iloc[-2]) if len(closes) >= 2 else None
    )

    daily_change = (
        latest_close - previous_close
        if previous_close is not None else None
    )

    daily_percent = (
        daily_change / previous_close * 100
        if previous_close not in (None, 0) else None
    )

    returns = closes.pct_change().dropna()

    daily_volatility = (
        float(returns.std() * 100)
        if len(returns) >= 2 else None
    )

    annualized_volatility = (
        daily_volatility * (252 ** 0.5)
        if daily_volatility is not None else None
    )

    currency = ticker.info.get("currency", "Unknown")

    return (
        history,
        latest_close,
        latest_volume,
        daily_change,
        daily_percent,
        daily_volatility,
        annualized_volatility,
        currency,
    )


# ---------------- MAIN DASHBOARD ----------------
st.title("Stock Market Dashboard")
st.markdown(
    '<p class="subtitle">'
    'Historical market data powered by Yahoo Finance and '
    'AI analysis powered by CrewAI + Groq.'
    '</p>',
    unsafe_allow_html=True,
)

st.divider()

if not stock_symbol:
    st.warning("Enter a valid stock ticker in the sidebar.")
    st.stop()

try:
    with st.spinner("Loading market data..."):
        (
            history,
            latest_close,
            latest_volume,
            daily_change,
            daily_percent,
            daily_volatility,
            annualized_volatility,
            currency,
        ) = get_market_data(stock_symbol)

except Exception as error:
    st.error(f"Could not load market data: {error}")
    st.stop()


# ---------------- PRICE METRICS ----------------
st.subheader(f"Market Overview · {stock_symbol}")

price_col, change_col, volume_col = st.columns(3)

price_col.metric(
    "Latest Available Close",
    f"{latest_close:,.2f} {currency}",
)

change_col.metric(
    "Daily Price Change",
    f"{daily_change:+,.2f}" if daily_change is not None else "N/A",
    delta=(
        f"{daily_percent:+.2f}%"
        if daily_percent is not None else None
    ),
)

volume_col.metric(
    "Latest Session Volume",
    f"{latest_volume:,} shares",
)

vol_col, annual_col, days_col = st.columns(3)

vol_col.metric(
    "Daily Volatility",
    f"{daily_volatility:.2f}%"
    if daily_volatility is not None else "N/A",
)

annual_col.metric(
    "Annualized Volatility",
    f"{annualized_volatility:.2f}%"
    if annualized_volatility is not None else "N/A",
)

days_col.metric(
    "Historical Sessions",
    str(len(history)),
)

st.caption(
    "Daily data reflects the latest available trading session, "
    "which may not be today's live price. Volatility is based on "
    "historical daily returns."
)

st.divider()


# ---------------- CHARTS ----------------
st.subheader("Historical Market Performance")

price_tab, volume_tab, data_tab = st.tabs([
    "📈 Closing Price",
    "📊 Trading Volume",
    "📋 Historical Data",
])

with price_tab:
    st.line_chart(
        history[["Close"]].rename(
            columns={"Close": "Closing Price"}
        ),
        use_container_width=True,
    )

with volume_tab:
    st.bar_chart(
        history[["Volume"]],
        use_container_width=True,
    )

with data_tab:
    display_data = history[
        ["Open", "High", "Low", "Close", "Volume"]
    ].copy()

    display_data.index = display_data.index.strftime("%Y-%m-%d")

    st.dataframe(
        display_data,
        use_container_width=True,
    )

    st.download_button(
        "⬇️ Download Historical Data (CSV)",
        data=display_data.to_csv().encode("utf-8"),
        file_name=f"{stock_symbol}_historical_data.csv",
        mime="text/csv",
    )



import re


# ---------------- AI REPORT HELPERS ----------------
def get_report_field(report, field):
    pattern = (
        rf"(?im)^\s*{re.escape(field)}\s*:\s*(.*?)\s*$"
    )
    match = re.search(pattern, report)
    return match.group(1).strip().strip("*") if match else "Not provided"


def get_report_section(report, heading):
    pattern = (
        rf"(?ims)^\s*{re.escape(heading)}\s*:?\s*\n"
        rf"(.*?)(?=^\s*[A-Z][A-Z\s]*:\s*$|\Z)"
    )
    match = re.search(pattern, report)
    return match.group(1).strip() if match else ""


# ---------------- AI AGENT ANALYSIS ----------------
st.divider()
st.subheader("🤖 AI Market Intelligence")

st.write(
    "Get a concise recommendation first, with supporting evidence "
    "and the full agent reports available when needed."
)

if analyze_button:
    try:
        with st.spinner(
            f"AI agents are analyzing {stock_symbol}..."
        ):
            result = stock_crew.kickoff(
                inputs={"stock": stock_symbol}
            )

        outputs = getattr(result, "tasks_output", [])
        final_report = str(getattr(result, "raw", result))

        analyst_report = (
            str(outputs[0].raw) if len(outputs) >= 1 else ""
        )

        trader_report = (
            str(outputs[1].raw) if len(outputs) >= 2 else final_report
        )

        # Normalize common Markdown emphasis around labels.
        clean_trader = trader_report.replace("**", "").replace("__", "")

        recommendation = get_report_field(
            clean_trader, "RECOMMENDATION"
        ).upper()

        confidence = get_report_field(
            clean_trader, "CONFIDENCE"
        ).title()

        risk = get_report_field(
            clean_trader, "RISK LEVEL"
        ).title()

        summary = get_report_section(
            clean_trader, "SUMMARY"
        )

        evidence = get_report_section(
            clean_trader, "KEY EVIDENCE"
        )

        risks = get_report_section(
            clean_trader, "RISKS"
        )

        what_changes = get_report_section(
            clean_trader, "WHAT COULD CHANGE THIS DECISION"
        )

        valid_recommendations = {"BUY", "SELL", "HOLD"}

        if recommendation not in valid_recommendations:
            recommendation = "REVIEW REPORT"

        # Main visual recommendation
        colors = {
            "BUY": "#16a34a",
            "SELL": "#dc2626",
            "HOLD": "#d97706",
            "REVIEW REPORT": "#64748b",
        }

        color = colors[recommendation]

        st.markdown(
            f"""
            <div style="
                background: linear-gradient(120deg, #172033, #111827);
                border: 1px solid #334155;
                border-radius: 16px;
                padding: 24px;
                margin: 12px 0 20px 0;
            ">
                <div style="
                    color: #94a3b8;
                    font-size: 13px;
                    letter-spacing: 1.5px;
                    font-weight: 600;
                ">
                    AI TRADING RECOMMENDATION · {stock_symbol}
                </div>
                <div style="
                    color: {color};
                    font-size: 42px;
                    font-weight: 800;
                    margin-top: 8px;
                    line-height: 1.2;
                ">
                    {recommendation}
                </div>
                <div style="
                    color: #cbd5e1;
                    font-size: 14px;
                    margin-top: 8px;
                ">
                    Based on the available market data and agent analysis.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # At-a-glance summary
        metric1, metric2, metric3 = st.columns(3)

        metric1.metric("Agent-assessed confidence", confidence)
        metric2.metric("Agent-assessed risk", risk)
        metric3.metric("Stock", stock_symbol)

        st.divider()

        # Executive summary
        st.markdown("###  The decision in brief")

        if summary:
            st.markdown(summary)
        else:
            st.info(
                "The agent did not provide a separately formatted "
                "summary. Open the detailed report below."
            )

        # Evidence and risk in compact columns
        left, right = st.columns(2)

        with left:
            st.markdown("####  Supporting evidence")
            if evidence:
                st.markdown(evidence)
            else:
                st.caption("No separate evidence section was returned.")

        with right:
            st.markdown("####  Key risks")
            if risks:
                st.markdown(risks)
            else:
                st.caption("No separate risk section was returned.")

        if what_changes:
            with st.expander(" What could change this decision?"):
                st.markdown(what_changes)

        # Full reports remain available but do not dominate the page.
        with st.expander(" Read the complete Trader report"):
            st.markdown(trader_report)

        with st.expander(" Read the complete Analyst report"):
            if analyst_report:
                st.markdown(analyst_report)
            else:
                st.info("No separate Analyst report was returned.")

        with st.expander(" Read the complete CrewAI output"):
            st.markdown(final_report)

        st.caption(
            "The recommendation, confidence, and risk level are "
            "AI-generated assessments, not verified predictions. "
            "Check the supporting evidence before drawing conclusions."
        )

    except Exception as error:
        st.error("The AI analysis could not be completed.")
        st.exception(error)