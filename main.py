import os
import boto3
from extract_market_data import fetch_and_upload
from transform_clean_data import transform_and_load

# Configuration AWS Glue
CRAWLER_NAME = "market-data-crawler"
AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-2")


def trigger_glue_crawler(crawler_name: str, region: str):
    """Déclenche le Crawler AWS Glue pour actualiser le catalogue Athena."""
    glue_client = boto3.client("glue", region_name=region)
    try:
        crawler = glue_client.get_crawler(Name=crawler_name)
        state = crawler["Crawler"]["State"]

        if state == "RUNNING":
            print(
                f"[!] Le Crawler '{crawler_name}' est déjà en cours d'exécution. Déclenchement ignoré."
            )
            return

        glue_client.start_crawler(Name=crawler_name)
        print(
            f"[+] Crawler Glue '{crawler_name}' déclenché avec succès !"
        )
    except Exception as e:
        print(f"[!] Erreur lors du déclenchement du crawler Glue : {e}")


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

    print("\n=== STEP 3: UPDATING AWS GLUE CATALOG ===")
    trigger_glue_crawler(CRAWLER_NAME, AWS_REGION)

    print("\n[+] Pipeline run complete.")


if __name__ == "__main__":
    run_pipeline()