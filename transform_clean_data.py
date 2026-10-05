import io
import os
import json
from datetime import datetime
import boto3
import pandas as pd

# --- CONFIGURATION AWS ---

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-2")
BUCKET_NAME = os.getenv("S3_BUCKET_NAME", "market-data-lake-wendyam")


def get_s3_client():
    return boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=AWS_REGION,
    )


def transform_and_load(ticker_symbol: str):
    s3 = get_s3_client()
    today_str = datetime.utcnow().strftime("%Y-%m-%d")
    raw_key = f"raw-zone/{ticker_symbol}_raw_{today_str}.json"

    print(f"[*] Téléchargement de s3://{BUCKET_NAME}/{raw_key}...")

    # 1. Lecture du JSON brut directement depuis S3
    response = s3.get_object(Bucket=BUCKET_NAME, Key=raw_key)
    raw_content = response["Body"].read().decode("utf-8")
    raw_json = json.loads(raw_content)

    # 2. Chargement dans un DataFrame Pandas
    df = pd.DataFrame(raw_json["data"])

    # 3. Nettoyage et ingénierie de variables
    df["Date"] = pd.to_datetime(df["Date"])
    df.sort_values(by="Date", ascending=True, inplace=True)

    # Sélection des colonnes utiles et suppression des valeurs manquantes
    cols = ["Date", "Open", "High", "Low", "Close", "Volume"]
    df = df[cols].dropna()

    # Calcul d'un indicateur technique : Moyenne mobile à 7 jours
    df["SMA_7d"] = df["Close"].rolling(window=7).mean().round(2)
    df["Ticker"] = ticker_symbol

    print(f"[+] Données transformées : {len(df)} lignes prêtes.")

    # 4. Conversion en mémoire au format Parquet
    parquet_buffer = io.BytesIO()
    df.to_parquet(parquet_buffer, index=False, engine="pyarrow")

    # 5. Envoi vers la clean-zone dans S3
    clean_key = f"clean-zone/{ticker_symbol}_clean_{today_str}.parquet"
    print(f"[*] Téléversement vers s3://{BUCKET_NAME}/{clean_key}...")

    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=clean_key,
        Body=parquet_buffer.getvalue(),
        ContentType="application/octet-stream",
    )

    print(f"[+] Succès : {clean_key} enregistré dans le Data Lake.")


if __name__ == "__main__":
    tickers = ["AAPL", "MSFT"]
    for ticker in tickers:
        try:
            transform_and_load(ticker)
        except Exception as e:
            print(f"[!] Erreur sur {ticker} : {e}")