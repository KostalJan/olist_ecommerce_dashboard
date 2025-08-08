import pandas as pd

def normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    if "order_status" in df.columns:
        df["order_status"] = df["order_status"].str.lower()
    return df
