# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 05:21:22 2026

@author: Dylan
"""
from pathlib import Path

import pandas as pd

from config.settings import INPUT_FILE, OUTPUT_FILE, MINIMUM_SCORE_TO_EXPORT
from utils.scorer import score_job, recommend


def main():
    output_path = Path(OUTPUT_FILE)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(INPUT_FILE)

    df["score"] = df.apply(
        lambda row: score_job(
            str(row["title"]),
            str(row["skills"]),
            str(row["description"]),
        ),
        axis=1,
    )

    df["recommendation"] = df["score"].apply(recommend)

    ranked_df = df.sort_values(by="score", ascending=False)
    filtered_df = ranked_df[ranked_df["score"] >= MINIMUM_SCORE_TO_EXPORT]

    filtered_df.to_csv(OUTPUT_FILE, index=False)

    print("\nJob ranking complete.\n")
    print(filtered_df[["title", "score", "recommendation"]].to_string(index=False))

    print("\nSummary:")
    print(f"Total jobs processed: {len(df)}")
    print(f"Jobs exported: {len(filtered_df)}")
    print(f"High Fit jobs: {(filtered_df['recommendation'] == 'High Fit').sum()}")
    print(f"Medium Fit jobs: {(filtered_df['recommendation'] == 'Medium Fit').sum()}")
    print(f"Low Fit jobs: {(filtered_df['recommendation'] == 'Low Fit').sum()}")
    print(f"\nSaved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()