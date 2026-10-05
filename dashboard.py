import os
import boto3
import streamlit as st
import pandas as pd
import plotly.express as px
from pyathena import connect
from dotenv import load_dotenv

load_dotenv()

# Page configuration
st.set_page_config(
    page_title="Market Data Lake Dashboard",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Market Data Lake Analytics")
st.caption("Live queries powered by Amazon Athena, AWS Glue & Amazon S3")

# AWS Athena configuration
# Try loading from Streamlit Cloud Secrets first, fall back to local .env (os.getenv)
try:
    AWS_ACCESS_KEY_ID = st.secrets["aws"]["aws_access_key_id"]
    AWS_SECRET_ACCESS_KEY = st.secrets["aws"]["aws_secret_access_key"]
    AWS_REGION = st.secrets["aws"].get("region_name", "us-east-2")
    S3_BUCKET = "market-data-lake-wendyam"
except Exception:
    AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
    AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-2")
    S3_BUCKET = os.getenv("S3_BUCKET_NAME", "market-data-lake-wendyam")

S3_STAGING_DIR = f"s3://{S3_BUCKET}/athena-results/"
DATABASE_NAME = "market_data_db"

@st.cache_data(ttl=300)
def run_query(query: str) -> pd.DataFrame:
    """Execute a SQL query against Amazon Athena."""
    
    # 1. Lock the session to your exact keys and region
    session = boto3.Session(
        aws_access_key_id=AWS_ACCESS_KEY_ID,           # <-- Removed os.getenv()
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,   # <-- Removed os.getenv()
        region_name=AWS_REGION                         # <-- Uses your region variable
    )
    
    # 2. Force the connection to use the primary workgroup and correct region
    conn = connect(
        s3_staging_dir=S3_STAGING_DIR,
        boto3_session=session,
        region_name="us-east-2",
        work_group="primary" 
    )
    
    return pd.read_sql(query, conn)

# Sidebar: Select Ticker
st.sidebar.header("Filter Options")
try:
    tickers_df = run_query(f"SELECT DISTINCT ticker FROM {DATABASE_NAME}.clean_zone ORDER BY ticker;")
    available_tickers = tickers_df["ticker"].dropna().tolist()
except Exception:
    available_tickers = ["AAPL", "MSFT"]

selected_ticker = st.sidebar.selectbox("Select Ticker", available_tickers)

# Query historical metrics for chosen ticker
data_query = f"""
SELECT 
    date,
    ticker,
    open,
    high,
    low,
    close,
    volume
FROM {DATABASE_NAME}.clean_zone
WHERE ticker = '{selected_ticker}'
ORDER BY date ASC;
"""

with st.spinner(f"Querying Athena for {selected_ticker}..."):
    try:
        df = run_query(data_query)
    except Exception as e:
        st.error(f"Error querying Athena: {e}")
        df = pd.DataFrame()

if not df.empty:
    df["date"] = pd.to_datetime(df["date"])
    
    # 7-day rolling moving average
    df["7_Day_MA"] = df["close"].rolling(window=7, min_periods=1).mean()

    # KPI Top Cards
    latest = df.iloc[-1]
    prev_close = df.iloc[-2]["close"] if len(df) > 1 else latest["close"]
    delta_close = latest["close"] - prev_close
    pct_change = (delta_close / prev_close) * 100

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Latest Close", f"${latest['close']:.2f}", f"{delta_close:+.2f} ({pct_change:+.2f}%)")
    col2.metric("Day High", f"${latest['high']:.2f}")
    col3.metric("Day Low", f"${latest['low']:.2f}")
    col4.metric("Volume", f"{int(latest['volume']):,}")

    st.markdown("---")

    # Interactive Price Chart
    fig = px.line(
        df,
        x="date",
        y=["close", "7_Day_MA"],
        labels={"value": "Price (USD)", "date": "Date", "variable": "Indicator"},
        title=f"{selected_ticker} Stock Price & 7-Day Moving Average"
    )
    fig.update_layout(hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)

    # Raw Data Expander
    with st.expander("🔍 View Raw Query Results"):
        st.dataframe(df.sort_values(by="date", ascending=False), use_container_width=True)
else:
    st.info("No data returned from Athena. Ensure the table `clean_zone` contains data.")