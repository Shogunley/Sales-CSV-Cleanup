"""Clean step: fix messy raw sales data before it can be trusted for analysis."""

import logging

import pandas as pd

logger = logging.getLogger(__name__)


def clean(df):
    """Strip whitespace, standardize text, parse dates, and drop bad rows."""
    df = df.copy()

    for col in ["region", "product"]:
        df[col] = df[col].astype(str).str.strip()
    df["region"] = df["region"].str.title()

    df["order_date"] = pd.to_datetime(df["order_date"], format="mixed")

    before = len(df)
    df = df.drop_duplicates(subset="order_id", keep="first")
    logger.info("Dropped %d duplicate order_id rows", before - len(df))

    before = len(df)
    df = df.dropna(subset=["quantity", "unit_price"])
    logger.info("Dropped %d rows with missing quantity/unit_price", before - len(df))

    before = len(df)
    df = df[df["quantity"] > 0]
    logger.info("Dropped %d rows with non-positive quantity", before - len(df))

    df["quantity"] = df["quantity"].astype(int)

    return df.reset_index(drop=True)
