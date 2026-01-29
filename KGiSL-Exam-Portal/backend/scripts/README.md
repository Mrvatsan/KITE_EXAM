# Backend Utility Scripts

This directory contains various utility scripts for checking data integrity and generating reports.

## Scripts

- `check_excel.py`: Verifies the structure and content of uploaded Excel files.
- `check_google_sheet.py`: Tests the connection to the configured Google Sheet.
- `generate_faculty_excel.py`: Generates a template Excel file for faculty data import.

## Usage

Run these scripts from the Django shell or directly with Python if they don't depend on Django models (or set up Django environment first).

Example:
```bash
python scripts/check_excel.py
```
