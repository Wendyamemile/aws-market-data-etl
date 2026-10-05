# AWS Market Data ETL Pipeline

[![ETL Pipeline Status](https://github.com/Wendyamemile/aws-market-data-etl/actions/workflows/pipeline.yml/badge.svg)](https://github.com/Wendyamemile/aws-market-data-etl/actions)

An automated, serverless ETL (Extract, Transform, Load) pipeline that ingests daily stock market data, processes it into an analytics-ready format, and stores it in an Amazon S3 Data Lake. 

This project demonstrates core data engineering principles, including API integration, data lake architecture (Bronze/Silver zones), columnar data storage optimization, and CI/CD workflow orchestration.

---

## 🏗️ Architecture and Workflow

This project implements a Data Lake architecture using Amazon S3:

1. **Extract (Bronze Layer):** 
   The `extract_market_data.py` script fetches daily historical stock data for target tickers (e.g., AAPL, MSFT) using the `yfinance` API. The raw data is appended with exact New York timezone timestamps to prevent file overwriting and is uploaded as JSON files to an Amazon S3 bucket under the `raw-zone/` prefix.

2. **Transform & Load (Silver Layer):** 
   The `transform_clean_data.py` script reads the raw JSON data, normalizes timestamps, cleans data types, and converts the payload into the highly compressed, columnar Parquet format. The cleaned, optimized files are uploaded to the `clean-zone/` prefix in S3, ready for SQL querying.

3. **Orchestration:** 
   The entire pipeline is fully automated using **GitHub Actions**. A cron schedule triggers the workflow every Monday through Friday at 9:00 PM UTC (after US markets close). 

---

## 🛠️ Technologies Used

* **Language:** Python 3.10
* **Cloud Provider:** Amazon Web Services (AWS)
* **Storage:** Amazon S3 (Data Lake)
* **Data Processing:** Pandas, Boto3, yfinance
* **CI/CD & Orchestration:** GitHub Actions

---

## 📂 Repository Structure

```text
aws-market-data-etl/
│
├── .github/workflows/
│   └── pipeline.yml          # GitHub Actions orchestration schedule
│
├── extract_market_data.py    # Fetches data and loads raw JSON to S3 raw-zone
├── transform_clean_data.py   # Cleans data and saves as Parquet to S3 clean-zone
├── main.py                   # Master script to run extraction and transformation sequentially
├── requirements.txt          # Python package dependencies
├── .gitignore                # Ignored system, data, and environment files
└── README.md                 # Project documentation