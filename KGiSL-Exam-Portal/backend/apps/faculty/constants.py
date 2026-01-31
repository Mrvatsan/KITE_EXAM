"""
Constants used for Faculty Data Google Sheets Integration.
"""

GOOGLE_SHEET_COLUMNS = [
    'EMP CODE', 
    'NAME', 
    'DEPT'
]

# Mapping from Sheet Column -> Model Field
COLUMN_MAPPING = {
    'EMP CODE': 'register_no',
    'NAME': 'name',
    'DEPT': 'department'
}
