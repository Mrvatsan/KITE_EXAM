import pandas as pd
import os

try:
    path = r'D:\ADMINFACULTYSTUDENT\Admin_Faculty_Student\KGiSL-Exam-Portal\FACULTYMODIFIED.xlsx'
    df = pd.read_excel(path)
    print("Columns found:", list(df.columns))
    print("First row:", df.iloc[0].to_dict())
except Exception as e:
    print(e)
