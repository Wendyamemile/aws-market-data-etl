from extract_market_data import fetch_and_upload
from transform_clean_data import transform_and_load


def run_pipeline():
    tickers = ["AAPL", "MSFT"]

    print("=== STEP 1: EXTRACTING & LOADING RAW DATA ===")
    for ticker in tickers:
        try:
            fetch_and_upload(ticker)
        except Exception as e:
            print(f"[!] Extraction error on {ticker}: {e}")

    print("\n=== STEP 2: TRANSFORMING & LOADING CLEAN DATA ===")
    for ticker in tickers:
        try:
            transform_and_load(ticker)
        except Exception as e:
            print(f"[!] Transformation error on {ticker}: {e}")

    print("\n[+] Pipeline run complete.")


if __name__ == "__main__":
    run_pipeline()