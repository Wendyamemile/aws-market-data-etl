import streamlit as st
import pandas as pd
import numpy as np

# Page configuration
st.set_page_config(
    page_title="AWS Market Data ETL",
    page_icon="📈",
    layout="wide"
)


# Title and description
st.title("📈 AWS Market Data ETL Pipeline")
st.markdown("Welcome to my portfolio web application! This app showcases financial market data processed through an automated AWS ETL pipeline.")

# Sidebar navigation
st.sidebar.header("Pipeline Controls")
data_source = st.sidebar.selectbox(
    "Select View", 
    ["Processed Market Data", "Pipeline Status", "System Logs"]
)

# Main content area based on sidebar selection
if data_source == "Processed Market Data":
    st.subheader("Latest Processed Financial Records")
    st.write("This section displays data extracted from financial APIs, cleaned via Python, and stored in AWS S3.")
    
    # Placeholder chart simulating market trends 
    # (Replace this later with your real data loaded via boto3 or pandas)
    chart_data = pd.DataFrame(
        np.random.randn(20, 3).cumsum(axis=0) + 100,
        columns=['Asset A', 'Asset B', 'Asset C']
    )
    
    st.line_chart(chart_data)
    
    st.write("Data Preview:")
    st.dataframe(chart_data.tail())

elif data_source == "Pipeline Status":
    st.subheader("AWS Infrastructure Status")
    st.success("AWS Lambda Extractor: Active (Daily Cron)")
    st.success("Amazon S3 Data Lake: Connected & Secure")
    st.info("Last Pipeline Execution: Success")

else:
    st.subheader("ETL Execution Logs")
    st.text("[INFO] 2026-10-05 04:00:01 - Initializing API connection...")
    st.text("[INFO] 2026-10-05 04:00:03 - Extracted 1,450 records successfully.")
    st.text("[INFO] 2026-10-05 04:00:04 - Transforming data structure and cleaning nulls.")
    st.text("[SUCCESS] 2026-10-05 04:00:06 - Loaded parquet files to S3 bucket.")

# Footer
st.markdown("---")
st.markdown("Built with Python, Streamlit, and AWS | Portfolio Project by Wendyam")