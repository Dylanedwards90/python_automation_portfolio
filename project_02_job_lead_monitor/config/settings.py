# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 05:32:05 2026

@author: Dylan
"""

KEYWORDS = {
    "python": 3,
    "selenium": 4,
    "automation": 3,
    "playwright": 3,
    "scraping": 2,
    "beautifulsoup": 2,
    "qa": 2,
    "testing": 1,
    "regression": 2,
    "csv": 1,
}

HIGH_FIT_THRESHOLD = 9
MEDIUM_FIT_THRESHOLD = 5

MINIMUM_SCORE_TO_EXPORT = 1
MINIMUM_RECOMMENDATION_TO_EXPORT = "Medium Fit"

INPUT_FILE = "input/jobs_input.csv"
INPUT_DIR = 'input'
PROCESSED_DIR = 'processed'
OUTPUT_DIR = "output"
OUTPUT_FILE_PREFIX = "ranked_jobs"
SUMMARY_FILE_PREFIX = "summary"
FAILED_DIR = 'failed'

TOP_RESULTS_TO_DISPLAY = 10
