"""Orchestrates the full extract -> clean -> transform -> load pipeline."""

import logging

from .clean import clean
from .config import CLEANED_PATH, RAW_PATH, SUMMARY_PATH
from .extract import extract
from .load import save_csv
from .transform import add_total_amount, monthly_region_summary

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)


def run_pipeline():
    logger.info("Reading raw sales data from %s", RAW_PATH)
    raw_df = extract(RAW_PATH)
    logger.info("Read %d raw rows", len(raw_df))

    cleaned_df = clean(raw_df)
    cleaned_df = add_total_amount(cleaned_df)
    logger.info("%d rows remain after cleaning", len(cleaned_df))

    summary_df = monthly_region_summary(cleaned_df)

    save_csv(cleaned_df, CLEANED_PATH)
    save_csv(summary_df, SUMMARY_PATH)
    logger.info("Saved cleaned data to %s and summary to %s", CLEANED_PATH, SUMMARY_PATH)


if __name__ == "__main__":
    run_pipeline()
