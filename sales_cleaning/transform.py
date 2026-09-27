"""Transform step: derive totals and roll cleaned rows up into a summary."""


def add_total_amount(df):
    """Add a total_amount = quantity * unit_price column."""
    df = df.copy()
    df["total_amount"] = df["quantity"] * df["unit_price"]
    return df


def monthly_region_summary(df):
    """Aggregate cleaned rows into order count and total sales per month/region."""
    df = df.copy()
    df["month"] = df["order_date"].dt.to_period("M").astype(str)

    summary = (
        df.groupby(["month", "region"], as_index=False)
        .agg(order_count=("order_id", "count"), total_sales=("total_amount", "sum"))
        .sort_values(["month", "region"])
        .reset_index(drop=True)
    )
    summary["total_sales"] = summary["total_sales"].round(2)
    return summary
