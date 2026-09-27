import pandas as pd

from sales_cleaning.transform import add_total_amount, monthly_region_summary


def test_add_total_amount():
    df = pd.DataFrame({"quantity": [2, 3], "unit_price": [1.5, 2.0]})

    result = add_total_amount(df)

    assert list(result["total_amount"]) == [3.0, 6.0]


def test_monthly_region_summary_groups_by_month_and_region():
    df = pd.DataFrame(
        {
            "order_id": [1, 2, 3],
            "order_date": pd.to_datetime(["2026-01-01", "2026-01-15", "2026-02-01"]),
            "region": ["North", "North", "South"],
            "quantity": [1, 2, 3],
            "unit_price": [10.0, 10.0, 5.0],
        }
    )
    df["total_amount"] = df["quantity"] * df["unit_price"]

    summary = monthly_region_summary(df)

    assert len(summary) == 2
    jan_north = summary[(summary["month"] == "2026-01") & (summary["region"] == "North")].iloc[0]
    assert jan_north["order_count"] == 2
    assert jan_north["total_sales"] == 30.0
