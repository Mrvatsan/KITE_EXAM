import pandas as pd
import requests
import io

try:
    url = "https://docs.google.com/spreadsheets/d/1gRWbJIgVEuOg6nJgNIVNDmrrSwNS_-i5yfYZWw42gnE/export?format=xlsx"
    print(f"Fetching: {url}")
    response = requests.get(url)
    response.raise_for_status()
    
    # Read as Excel
    excel_file = io.BytesIO(response.content)
    all_sheets = pd.read_excel(excel_file, sheet_name=None)
    
    print(f"Sheets found: {list(all_sheets.keys())}")
    
    total_rows = 0
    for name, df in all_sheets.items():
        print(f"Sheet '{name}': {len(df)} rows")
        total_rows += len(df)
        
    print(f"Total Combined Rows: {total_rows}")
except Exception as e:
    print(e)
