# Sales CSV Cleanup Pipeline

A small data cleaning pipeline that takes a messy raw sales CSV (the kind of
file that comes out of a manual export — inconsistent casing, stray
whitespace, mixed date formats, duplicate rows, missing values, obvious data
entry errors) and turns it into clean, analysis-ready data plus a monthly
summary report.

Built as a hands-on data engineering practice project to work through a
common real-world task: raw data is rarely clean, and turning it into
something trustworthy is its own pipeline.

## The messy input

[`data/raw/sales_raw.csv`](data/raw/sales_raw.csv) is a sample of 24 sales
orders with deliberately realistic problems:

- Inconsistent region casing (`North`, `NORTH`, `south`, ` south `)
- Stray leading/trailing whitespace (`"Pen "`, `" south "`)
- Two different date formats (`2026-01-05` and `01/07/2026`)
- Missing values (`quantity` or `unit_price` blank on some rows)
- A duplicate order (`order_id` 1002 appears twice, identical)
- A data entry error (a negative `quantity`)

## Architecture

```
                extract.py        clean.py              transform.py          load.py
sales_raw.csv ─────►  raw rows ─────►  clean rows ─────►  + total_amount ─────►  sales_cleaned.csv
                                                            + monthly summary ─────►  monthly_region_summary.csv
```

- **`sales_cleaning/extract.py`** — reads the raw CSV into a DataFrame.
- **`sales_cleaning/clean.py`** — strips whitespace, standardizes region
  names to title case, parses both date formats into real dates, drops
  duplicate orders, drops rows missing `quantity`/`unit_price`, and drops
  rows with a non-positive `quantity`. Logs how many rows each step removes.
- **`sales_cleaning/transform.py`** — adds a `total_amount` column
  (`quantity * unit_price`) and rolls the cleaned rows up into an
  order-count / total-sales summary per month and region.
- **`sales_cleaning/load.py`** — writes the cleaned rows and the summary out
  to `data/processed/`.
- **`sales_cleaning/pipeline.py`** — runs the four steps in order and logs
  progress.
- **`tests/`** — unit tests for the cleaning and transform logic, using small
  hand-built DataFrames so they run instantly with no file I/O.

## Setup

```bash
pip install -r requirements.txt
```

## Usage

Run from the project root (so `data/raw` and `data/processed` resolve
correctly):

```bash
python -m sales_cleaning.pipeline
```

This produces:
- `data/processed/sales_cleaned.csv` — one row per valid order, with `total_amount`
- `data/processed/monthly_region_summary.csv` — order count and total sales per month/region

Run the tests:

```bash
pytest
```

## Possible next steps

- Add more validation rules (e.g. flag orders above a price threshold for review)
- Write cleaned data to a database instead of a CSV
- Add a data quality report (rows dropped, by reason) as a pipeline output
- Parameterize the pipeline to accept any raw CSV path via the command line
