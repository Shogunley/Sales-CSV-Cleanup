import pandas as pd

from sales_cleaning.clean import clean


def test_clean_removes_duplicates_missing_and_invalid_rows():
    raw = pd.DataFrame(
        {
            "order_id": [1, 1, 2, 3, 4],
            "order_date": ["2026-01-01", "2026-01-01", "2026-01-02", "2026-01-03", "01/04/2026"],
            "region": ["North", "North", " south ", "EAST", "west"],
            "product": ["Pen", "Pen", "Notebook ", "Stapler", "Chair"],
            "quantity": [5, 5, None, -2, 3],
            "unit_price": [1.0, 1.0, 2.0, 3.0, 4.0],
        }
    )

    cleaned = clean(raw)

    # order_id 1 is a duplicate (keep 1 row), 2 has missing quantity,
    # 3 has a negative quantity -> only order_id 1 and 4 should remain
    assert len(cleaned) == 2
    assert set(cleaned["order_id"]) == {1, 4}
    assert set(cleaned["region"]) == {"North", "West"}
    assert pd.api.types.is_datetime64_any_dtype(cleaned["order_date"])


def test_clean_strips_whitespace_and_title_cases_region():
    raw = pd.DataFrame(
        {
            "order_id": [1],
            "order_date": ["2026-01-01"],
            "region": [" south "],
            "product": ["Pen "],
            "quantity": [10],
            "unit_price": [1.5],
        }
    )

    cleaned = clean(raw)

    assert cleaned.loc[0, "region"] == "South"
    assert cleaned.loc[0, "product"] == "Pen"
