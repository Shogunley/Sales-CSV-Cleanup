"""Extract step: read the raw sales CSV into a DataFrame."""

import pandas as pd


def extract(raw_path):
    return pd.read_csv(raw_path)
