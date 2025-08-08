import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from .theme import use_theme

def plot_order_status_counts(df: pd.DataFrame, outfile=None):
    use_theme()
    ax = sns.countplot(data=df, x="order_status", order=df["order_status"].value_counts().index)
    ax.set(xlabel="Order status", ylabel="Orders", title="Order status distribution")
    ax.tick_params(axis="x", rotation=30)
    plt.tight_layout()
    if outfile:
        plt.savefig(outfile, dpi=150)
    return ax

def plot_orders_by_month(df: pd.DataFrame, outfile=None):
    use_theme()
    tmp = (df.assign(order_month=df["order_purchase_timestamp"]
                     .dt.tz_convert(None).dt.to_period("M").astype(str))
             .groupby("order_month").size().reset_index(name="orders"))
    ax = sns.lineplot(data=tmp, x="order_month", y="orders", marker="o")
    ax.set(title="Orders over time (monthly)", xlabel="Month", ylabel="Orders")
    ax.tick_params(axis="x", rotation=45)
    plt.tight_layout()
    if outfile:
        plt.savefig(outfile, dpi=150)
    return ax


def plot_delivery_delay_hist(df: pd.DataFrame, outfile=None):
    use_theme()
    if "delivery_delay_days" not in df.columns:
        raise ValueError("Chybí sloupec delivery_delay_days – zavolej add_delivery_delay_days().")
    ax = sns.histplot(data=df, x="delivery_delay_days", bins=40, kde=True)
    ax.set(
        title="Delivery delay distribution (days)",
        xlabel="Days vs. estimated date (− = early, + = late)",
        ylabel="Orders",
    )
    plt.tight_layout()
    if outfile:
        plt.savefig(outfile, dpi=150)
    return ax

def plot_orders_top_states(df_states: pd.DataFrame, outfile=None):
    use_theme()
    ax = sns.barplot(data=df_states, x="customer_state", y="orders")
    ax.set(title="Top states by number of orders", xlabel="State", ylabel="Orders")
    ax.tick_params(axis="x", rotation=45)
    plt.tight_layout()
    if outfile:
        plt.savefig(outfile, dpi=150)
    return ax


def plot_orders_by_dow(df_dow: pd.DataFrame, outfile=None):
    use_theme()
    ax = sns.barplot(data=df_dow, x="dow", y="orders")
    ax.set(title="Orders by Day of Week", xlabel="", ylabel="Orders")
    ax.tick_params(axis="x", rotation=25)
    plt.tight_layout()
    if outfile:
        plt.savefig(outfile, dpi=150)
    return ax

def plot_cancel_rate_by_month(df_cr: pd.DataFrame, outfile=None):
    use_theme()
    ax = sns.lineplot(data=df_cr, x="order_month", y="cancel_rate", marker="o")
    ax.set(title="Monthly Cancel Rate", xlabel="Month", ylabel="Cancel rate")
    ax.yaxis.set_major_formatter(lambda v, pos: f"{v:.0%}")
    ax.tick_params(axis="x", rotation=45)
    plt.tight_layout()
    if outfile:
        plt.savefig(outfile, dpi=150)
    return ax