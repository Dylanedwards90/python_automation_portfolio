# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 05:21:22 2026

@author: Dylan
"""
from pathlib import Path
from datetime import datetime
import argparse

import pandas as pd

from config.settings import (
    INPUT_FILE, 
    OUTPUT_DIR, 
    OUTPUT_FILE_PREFIX, 
    SUMMARY_FILE_PREFIX,
    MINIMUM_RECOMMENDATION_TO_EXPORT,  
    MINIMUM_SCORE_TO_EXPORT,
    TOP_RESULTS_TO_DISPLAY
)
from utils.scorer import score_job, recommend, get_matched_keywords

timestamp = datetime.now().strftime("%Y-%m-%d")

RECOMMENDATION_ORDER = {
    "Low Fit": 1,
    "Medium Fit": 2,
    "High Fit": 3,
}

def parse_args():
    parser = argparse.ArgumentParser(
        description="Rank job leads from a CSV file."
    )
    parser.add_argument(
        "--input",
        dest="input_file",
        default=INPUT_FILE,
        help="Path to the input CSV file.",
    )
    return parser.parse_args()

def build_output_file_path() -> Path:
    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir/f"{OUTPUT_FILE_PREFIX}_{timestamp}.csv"
    
def build_summary_file_path() -> Path:
    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir/f'{SUMMARY_FILE_PREFIX}_{timestamp}.txt'

def write_summary_file(
    summary_file: Path,
    total_jobs: int,
    jobs_after_dedup: int,
    exported_jobs: int,
    high_fit_count: int,
    medium_fit_count: int,
    low_fit_count: int,
    minimum_recommendation: str,
    csv_file: Path,
) -> None:
    summary_text = (
        "Job Lead Monitor Summary\n"
        "========================\n"
        f"Total jobs processed: {total_jobs}\n"
        f"Jobs after deduplication: {jobs_after_dedup}\n"
        f"Jobs exported: {exported_jobs}\n"
        f"High Fit jobs: {high_fit_count}\n"
        f"Medium Fit jobs: {medium_fit_count}\n"
        f"Low Fit jobs: {low_fit_count}\n"
        f"Minimum recommendation exported: {minimum_recommendation}\n"
        f"CSV output file: {csv_file.name}\n"
    )

    summary_file.write_text(summary_text, encoding="utf-8")


def main():
    args = parse_args()
    input_file = args.input_file
    
    output_file = build_output_file_path()
    summary_file = build_summary_file_path()

    df = pd.read_csv(input_file)

    df = df.drop_duplicates(subset=["title", "description"]).copy()
    jobs_after_dedup = len(df)

    df["matched_keywords"] = df.apply(
        lambda row: ", ".join(
            get_matched_keywords(
                str(row["title"]),
                str(row["skills"]),
                str(row["description"]),
            )
        ),
        axis=1,
    )

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

    filtered_df = ranked_df[
        (ranked_df["score"] >= MINIMUM_SCORE_TO_EXPORT)
        & (
            ranked_df["recommendation"].map(RECOMMENDATION_ORDER)
            >= RECOMMENDATION_ORDER[MINIMUM_RECOMMENDATION_TO_EXPORT]
        )
    ]

    filtered_df.to_csv(output_file, index=False)

    high_fit_count = (filtered_df["recommendation"] == "High Fit").sum()
    medium_fit_count = (filtered_df["recommendation"] == "Medium Fit").sum()
    low_fit_count = (filtered_df["recommendation"] == "Low Fit").sum()

    write_summary_file(
        summary_file=summary_file,
        total_jobs=len(df),
        jobs_after_dedup=jobs_after_dedup,
        exported_jobs=len(filtered_df),
        high_fit_count=high_fit_count,
        medium_fit_count=medium_fit_count,
        low_fit_count=low_fit_count,
        minimum_recommendation=MINIMUM_RECOMMENDATION_TO_EXPORT,
        csv_file=output_file,
    )

    top_results_df = filtered_df.head(TOP_RESULTS_TO_DISPLAY)

    print("\nJob ranking complete.\n")
    print(f"Top {TOP_RESULTS_TO_DISPLAY} job results:\n")
    print(
        top_results_df[
            ["title", "score", "recommendation", "matched_keywords"]
        ].to_string(index=False)
    )

    print("\nSummary:")
    print(f"Total jobs processed: {len(df)}")
    print(f"Jobs exported: {len(filtered_df)}")
    print(f"High Fit jobs: {high_fit_count}")
    print(f"Medium Fit jobs: {medium_fit_count}")
    print(f"Low Fit jobs: {low_fit_count}")
    print(f"Minimum recommendation exported: {MINIMUM_RECOMMENDATION_TO_EXPORT}")
    print(f"Top results displayed: {TOP_RESULTS_TO_DISPLAY}")
    print(f"\nSaved CSV to: {output_file}")
    print(f"Saved summary to: {summary_file}")


if __name__ == "__main__":
    main()