# Student Performance and Study-Hours Dashboard

A menu-driven Python application for managing student assessment records and analysing study hours and scores.

## Features
- Add, insert, delete, modify and display multiple student records
- Input validation and duplicate-ID prevention
- CSV and JSON persistence (`student_data.csv`, `student_data.json`)
- Letter-grade calculation
- NumPy descriptive statistics
- Pandas course-wise summaries
- Matplotlib scatter plot and score histogram
- IQR and MAD score-outlier detection
- Pearson correlation before and after IQR filtering
- Synthetic 15-record demonstration dataset

## Requirements
- Python 3.9 or later
- Packages listed in `requirements.txt`

## Setup
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
source .venv/bin/activate

python -m pip install -r requirements.txt
```

## Run
```bash
python student_performance_dashboard.py
```
Choose option `12` to create the demonstration dataset (only when the database is empty). Then use options 7–10 to view analyses and graphs.

## Data files
The application reads `student_data.csv` first. If that file does not exist, it tries `student_data.json`. Saving writes both formats. The generated dataset is synthetic and must not be represented as real student observations.

## Repository contents
- `student_performance_dashboard.py` — application source code
- `requirements.txt` — Python dependencies
- `Student_Performance_and_Study_Hours_Dashboard_Report.pdf` — project report
- `Student_Performance_and_Study_Hours_Dashboard_Report.docx` — editable report
- `student_data.csv`, `student_data.json` — sample synthetic data
- `.gitignore` — excludes local environments and cache files

## GitHub submission
1. Create a **public** GitHub repository named `Student_Performance_and_Study_Hours_Dashboard`.
2. Upload/push all files in this project folder.
3. Confirm the repository is publicly accessible.
4. Submit the repository URL in the class Google Sheet. As instructed, only one team member should submit the link for the group.

## Note
The code corrects the stray trailing period after `main()` in the pasted source so the Python file runs. The report is based on the supplied revised report; verify all team details and run the test cases in your own environment before submission.
