import pandas as pd
import numpy as np

def add_order_date_parts(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    col = "order_purchase_timestamp"
    if col in df.columns:
        s = df[col].dt.tz_convert(None) if hasattr(df[col].dtype, "tz") else df[col]
        df["order_date"] = s.dt.date
        df["order_month"] = s.dt.to_period("M").astype(str)
        df["order_year"] = s.dt.year
        df["dow"] = s.dt.day_name()
    return df


def add_delivery_delay_days(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    cols = ["order_delivered_customer_date", "order_estimated_delivery_date"]
    if not all(c in df.columns for c in cols):
        return df
    delivered = df["order_delivered_customer_date"]
    eta = df["order_estimated_delivery_date"]
    # rozdíl ve dnech (může být i záporný = doručeno dřív)
    diff = (delivered - eta).dt.total_seconds() / 86400.0
    df["delivery_delay_days"] = np.round(diff, 1)
    return df