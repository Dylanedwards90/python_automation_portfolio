# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 05:21:22 2026

@author: Dylan
"""
from pathlib import Path
from datetime import datetime
import argparse
import sys
import shutil
import pandas as pd

from config.settings import (
    INPUT_FILE, 
    OUTPUT_DIR, 
    INPUT_DIR,
    PROCESSED_DIR,
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

def build_output_file_path(timestamp: str, input_file: Path) -> Path:
    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir / f"{input_file.stem}_{OUTPUT_FILE_PREFIX}_{timestamp}.csv"


def build_summary_file_path(timestamp: str, input_file: Path) -> Path:
    output_dir = Path(OUTPUT_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir / f"{input_file.stem}_{SUMMARY_FILE_PREFIX}_{timestamp}.txt"

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
    input_file: str,
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

def load_input_file(input_file: Path) -> pd.DataFrame:
    if not input_file.exists():
        print(f"Error: Input file not found: {input_file}")
        sys.exit(1)

    if input_file.suffix.lower() != ".csv":
        print(f"Error: Only CSV files are supported: {input_file}")
        sys.exit(1)

    try:
        df = pd.read_csv(input_file)
    except Exception as exc:
        print(f"Error: Failed to read CSV file '{input_file}': {exc}")
        sys.exit(1)

    required_columns = {"title", "skills", "description"}
    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        print(
            "Error: Missing required columns: "
            + ", ".join(sorted(missing_columns))
        )
        sys.exit(1)

    return df

def process_dataframe(df: pd.DataFrame) -> pd.DataFrame:
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

    return filtered_df

def move_to_processed(input_file: Path) -> None:
    processed_dir = Path(PROCESSED_DIR)
    processed_dir.mkdir(parents=True, exist_ok=True)

    destination = processed_dir / input_file.name
    shutil.move(str(input_file), str(destination))


def process_file(input_file: Path) -> None:
    output_file = build_output_file_path(timestamp, input_file)
    summary_file = build_summary_file_path(timestamp, input_file)

    df = load_input_file(input_file)
    if df is None:
        return

    total_jobs = len(df)
    df = df.drop_duplicates(subset=["title", "description"]).copy()
    jobs_after_dedup = len(df)

    filtered_df = process_dataframe(df)
    filtered_df.to_csv(output_file, index=False)

    high_fit_count = (filtered_df["recommendation"] == "High Fit").sum()
    medium_fit_count = (filtered_df["recommendation"] == "Medium Fit").sum()
    low_fit_count = (filtered_df["recommendation"] == "Low Fit").sum()

    write_summary_file(
        summary_file=summary_file,
        total_jobs=total_jobs,
        jobs_after_dedup=jobs_after_dedup,
        exported_jobs=len(filtered_df),
        high_fit_count=high_fit_count,
        medium_fit_count=medium_fit_count,
        low_fit_count=low_fit_count,
        minimum_recommendation=MINIMUM_RECOMMENDATION_TO_EXPORT,
        csv_file=output_file,
        input_file=str(input_file),
    )

    top_results_df = filtered_df.head(TOP_RESULTS_TO_DISPLAY)

    print(f"\nFinished processing: {input_file.name}\n")
    if not top_results_df.empty:
        print(
            top_results_df[
                ["title", "score", "recommendation", "matched_keywords"]
            ].to_string(index=False)
        )
    else:
        print("No matching jobs to display.")

    print(f"\nSaved CSV to: {output_file}")
    print(f"Saved summary to: {summary_file}")

    move_to_processed(input_file)
    print(f"Moved input file to: {PROCESSED_DIR}/{input_file.name}\n")


def main():
    input_dir = Path(INPUT_DIR)
    input_dir.mkdir(parents=True, exist_ok=True)

    csv_files = list(input_dir.glob("*.csv"))

    if not csv_files:
        print(f"No CSV files found in '{INPUT_DIR}'.")
        sys.exit(0)

    for csv_file in csv_files:
        process_file(csv_file)


if __name__ == "__main__":
    main()