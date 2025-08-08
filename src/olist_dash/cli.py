import argparse
from pathlib import Path
from .io.load import read_orders, read_customers
from .io.paths import REPORTS
from .processing.clean import normalize_columns
from .processing.features import add_order_date_parts, add_delivery_delay_days
from .processing.aggregates import orders_per_state, orders_by_dow, cancel_rate_by_month
from .viz.plots import (
    plot_order_status_counts,
    plot_orders_by_month,
    plot_delivery_delay_hist,
    plot_orders_top_states,
    plot_orders_by_dow,
    plot_cancel_rate_by_month,
)

def main():
    parser = argparse.ArgumentParser(description="Generate Olist reports")
    parser.add_argument("--report-dir", default=str(REPORTS / "latest"))
    args = parser.parse_args()

    out = Path(args.report_dir)
    out.mkdir(parents=True, exist_ok=True)

    df = read_orders()
    df = normalize_columns(df)
    df = add_order_date_parts(df)

    # Delivery delay
    df = add_delivery_delay_days(df)
    plot_delivery_delay_hist(df, outfile=out / "delivery_delay_hist.png")

    # Top states
    customers = read_customers()
    df_states = orders_per_state(df, customers, top_n=10)
    plot_orders_top_states(df_states, outfile=out / "orders_top_states.png")

    # Orders by DOW
    df_dow = orders_by_dow(df)
    plot_orders_by_dow(df_dow, outfile=out / "orders_by_dow.png")

    # Cancel rate by month
    df_cr = cancel_rate_by_month(df)
    plot_cancel_rate_by_month(df_cr, outfile=out / "cancel_rate_by_month.png")

    plot_order_status_counts(df, outfile=out / "order_status.png")
    plot_orders_by_month(df, outfile=out / "orders_monthly.png")

if __name__ == "__main__":
    main()
