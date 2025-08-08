import pandas as pd
from .paths import RAW

def read_orders() -> pd.DataFrame:
    path = RAW / "olist_orders_dataset.csv"
    df = pd.read_csv(path)
    for col in ["order_purchase_timestamp", "order_approved_at", "order_delivered_carrier_date",
                "order_delivered_customer_date", "order_estimated_delivery_date"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce", utc=True)
    return df

def read_customers() -> pd.DataFrame:
    path = RAW / "olist_customers_dataset.csv"
    return pd.read_csv(path)

def read_geolocation() -> pd.DataFrame:
    path = RAW / "olist_geolocation_dataset.csv"
    return pd.read_csv(path)
