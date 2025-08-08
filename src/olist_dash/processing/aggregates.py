import pandas as pd

def orders_per_state(orders: pd.DataFrame, customers: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    # join přes customer_id → customer_state
    if "customer_id" not in orders.columns or "customer_id" not in customers.columns:
        return pd.DataFrame(columns=["customer_state", "orders"])
    tmp = (orders[["order_id", "customer_id"]]
           .merge(customers[["customer_id", "customer_state"]], on="customer_id", how="left"))
    out = (tmp.groupby("customer_state")["order_id"]
             .nunique()
             .reset_index(name="orders")
             .sort_values("orders", ascending=False)
             .head(top_n))
    return out

def orders_by_dow(df_orders: pd.DataFrame) -> pd.DataFrame:
    """Počty objednávek podle dne v týdnu (Po–Ne)."""
    if "order_purchase_timestamp" not in df_orders.columns:
        return pd.DataFrame(columns=["dow", "orders"])
    s = df_orders["order_purchase_timestamp"]
    s = s.dt.tz_convert(None) if hasattr(s.dtype, "tz") else s
    tmp = (pd.DataFrame({"dow": s.dt.day_name()})
             .value_counts()
             .rename("orders")
             .reset_index())
    # pevné pořadí Po–Ne (v angličtině Monday–Sunday)
    cat = pd.CategoricalDtype(
        ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"],
        ordered=True
    )
    tmp["dow"] = tmp["dow"].astype(cat)
    return tmp.sort_values("dow").reset_index(drop=True)

def cancel_rate_by_month(df_orders: pd.DataFrame) -> pd.DataFrame:
    """Měsíční míra stornování: canceled / (delivered+canceled+shipped+invoiced+processing...)."""
    if not {"order_status", "order_purchase_timestamp"}.issubset(df_orders.columns):
        return pd.DataFrame(columns=["order_month", "cancel_rate"])
    s = df_orders["order_purchase_timestamp"]
    s = s.dt.tz_convert(None) if hasattr(s.dtype, "tz") else s
    df = df_orders.assign(order_month=s.dt.to_period("M").astype(str))
    # vybereme „relevantní“ stavy (můžeš si upravit podle svého datasetu)
    relevant = df[df["order_status"].isin([
        "delivered", "canceled", "shipped", "invoiced", "processing", "approved", "created"
    ])]
    grp = (relevant
           .groupby(["order_month", "order_status"])
           .size()
           .unstack(fill_value=0))
    canceled = grp.get("canceled", 0)
    total = grp.sum(axis=1).replace(0, pd.NA)
    out = (canceled / total).rename("cancel_rate").reset_index()
    return out