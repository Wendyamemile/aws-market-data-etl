# AWS Market Data ETL Pipeline

[![ETL Pipeline Status](https://github.com/Wendyamemile/aws-market-data-etl/actions/workflows/pipeline.yml/badge.svg)](https://github.com/Wendyamemile/aws-market-data-etl/actions)
[![Live Demo](https://img.shields.io/badge/Live%20Dashboard-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)](https://aws-market-data-etl-3xnorj7ohfcxuxshp2o4iq.streamlit.app/)

An automated, serverless ETL (Extract, Transform, Load) pipeline that ingests daily stock market data, processes it into an analytics-ready format, stores it in an Amazon S3 Data Lake, and visualizes it via an interactive Streamlit dashboard. 

This project demonstrates core data engineering principles, including API integration, data lake architecture (Bronze/Silver zones), columnar data storage optimization, automated schema cataloging, CI/CD workflow orchestration, and serverless data visualization.

---

## 🏗️️ Architecture and Workflow

This project implements a Data Lake architecture using Amazon S3, AWS Glue, and Amazon Athena:

1. **Extract (Bronze Layer):** 
   The `extract_market_data.py` script fetches daily historical stock data for target tickers (e.g., AAPL, MSFT) using the `yfinance` API. The raw data is appended with exact New York timezone timestamps to prevent file overwriting and is uploaded as JSON files to an Amazon S3 bucket under the `raw-zone/` prefix.

2. **Transform & Load (Silver Layer):** 
   The `transform_clean_data.py` script reads the raw JSON data, normalizes timestamps, cleans data types, and converts the payload into the highly compressed, columnar Parquet format. The cleaned, optimized files are uploaded to the `clean-zone/` prefix in S3, ready for SQL querying.

3. **Automated Cataloging (AWS Glue):** 
   Upon successful transformation, `main.py` uses `boto3` to trigger an AWS Glue Crawler. The crawler automatically scans the new Parquet files, infers the schema, and registers the table in the AWS Glue Data Catalog.

4. **Analytics (Amazon Athena):**
   With the data cataloged, Amazon Athena provides a serverless SQL interface, allowing for instant, direct querying of the S3 market data without provisioning a database.

5. **Visualization (Dashboard):**
   A Streamlit application (`dashboard.py`) securely connects to Athena to query the cleaned data in real-time, rendering interactive financial candlestick charts and moving averages using Plotly. The application is deployed globally via **Streamlit Community Cloud**.

6. **Orchestration:** 
   The entire ETL pipeline is fully automated using **GitHub Actions**. A cron schedule triggers the workflow every Monday through Friday at 9:00 PM UTC (after US markets close). 

---

## 🛠️ Technologies Used

- **Language:** Python 3.10
- **Cloud Provider:** Amazon Web Services (AWS)
- **Storage & Analytics:** Amazon S3 (Data Lake), AWS Glue (Data Catalog), Amazon Athena (Serverless SQL)
- **Data Processing:** Pandas, Boto3, yfinance
- **Visualization & UI:** Streamlit, Streamlit Community Cloud, Plotly, PyAthena
- **CI/CD & Orchestration:** GitHub Actions

---

## 📂 Repository Structure

```text
aws-market-data-etl/
│
├── .github/workflows/
│   └── pipeline.yml          # GitHub Actions orchestration schedule
│
├── dashboard.py              # Streamlit dashboard and Athena connection UI
├── extract_market_data.py    # Fetches data and loads raw JSON to S3 raw-zone
├── transform_clean_data.py   # Cleans data and saves as Parquet to S3 clean-zone
├── main.py                   # Master script to run extraction, transformation, and trigger Glue
├── requirements.txt          # Python package dependencies
├── .env                      # Local environment variables (ignored in Git)
├── .gitignore                # Ignored system, data, and environment files
└── README.md                 # Project documentation
```

## 🚀 Getting Started & Local Setup

### 1. Clone the Repository
```bash
git clone https://github.com/Wendyamemile/aws-market-data-etl.git
cd aws-market-data-etl
```

### 2. Configure AWS Environment Variables
```text
Create a .env file in the root directory. (Note: The IAM user associated with these credentials must have read/write access to S3, and execution permissions for Glue and Athena).
```

```bash
AWS_ACCESS_KEY_ID="your_access_key_here"
AWS_SECRET_ACCESS_KEY="your_secret_key_here"
AWS_DEFAULT_REGION="us-east-2"
S3_BUCKET_NAME="market-data-lake-wendyam"
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the ETL Pipeline
```text
To populate your S3 bucket and trigger the Glue crawler locally:
```

```bash
python main.py
```

### 5. Run the Dashboard Locally
```bash
streamlit run dashboard.py
```

### 🌐 Streamlit Cloud Deployment
```text
1. Connect your GitHub repository (aws-market-data-etl) to Streamlit Cloud.
2. Set the Main file path to dashboard.py.
3. Under App settings → Secrets, paste your AWS IAM credentials at the root level (no headers):
```

```toml
AWS_ACCESS_KEY_ID = "your_access_key_here"
AWS_SECRET_ACCESS_KEY = "your_secret_key_here"
AWS_DEFAULT_REGION = "us-east-2"
S3_BUCKET_NAME = "market-data-lake-wendyam"
```