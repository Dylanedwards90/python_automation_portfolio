# Job Lead Monitor

A Python automation project that reads job listings from CSV, scores them against target keywords, and exports a ranked list of opportunities.

## Features
- Reads job data from CSV
- Scores each listing based on configurable keywords
- Labels jobs as High Fit, Medium Fit, or Low Fit
- Exports ranked results to CSV
- Prints a simple summary in the console

## Tech Stack
- Python
- Pandas

## Run
powershell
py main.py


## Windows Quick Start
1. Drop one or more CSV files into the `input` folder.
2. Double-click `run_job_monitor.bat`.
3. Review the ranked CSV and summary report in the `output` folder.
4. Processed input files will be moved to the `processed` folder.