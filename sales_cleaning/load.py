"""Load step: write a DataFrame out to CSV, creating folders as needed."""

import os


def save_csv(df, path):
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    df.to_csv(path, index=False)
