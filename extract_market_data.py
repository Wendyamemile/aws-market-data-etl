from datetime import datetime
import os
import json
import boto3
import yfinance as yf

# AWS CONFIGURATION

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-2")
BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "market-data-lake-wendyam")


def fetch_and_upload(ticker_symbol: str):
  print(f"[*] Ingesting {ticker_symbol}...")
  hist = yf.Ticker(ticker_symbol).history(period="1mo")
  hist.reset_index(inplace=True)
  hist["Date"] = hist["Date"].dt.strftime("%Y-%m-%d")

  payload = {
      "ticker": ticker_symbol,
      "extracted_at_utc": datetime.utcnow().isoformat(),
      "record_count": len(hist),
      "data": hist.to_dict(orient="records"),
  }

  # Added %H%M%S to include Hour, Minute, and Second in the filename
  today_str = datetime.utcnow().strftime("%Y-%m-%d_%H%M%S")
  s3_key = f"raw-zone/{ticker_symbol}_raw_{today_str}.json"

  s3 = boto3.client(
      "s3",
      aws_access_key_id=AWS_ACCESS_KEY,
      aws_secret_access_key=AWS_SECRET_KEY,
      region_name=AWS_REGION,
  )

  s3.put_object(
      Bucket=BUCKET_NAME,
      Key=s3_key,
      Body=json.dumps(payload, indent=2),
      ContentType="application/json",
  )
  print(f"[+] Loaded: s3://{BUCKET_NAME}/{s3_key}")


if __name__ == "__main__":
  for symbol in ["AAPL", "MSFT"]:
    fetch_and_upload(symbol)