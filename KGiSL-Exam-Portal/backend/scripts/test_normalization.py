from exams.utils import normalize_department_name

# Test normalization with various inputs
test_cases = [
    # Standard formats
    ('AI&ML', 'AI&ML'),
    ('AI&DS', 'AI&DS'),
    ('CSE', 'CSE'),
    ('ECE', 'ECE'),
    ('IT', 'IT'),
    ('MECH', 'MECH'),
    ('R&A', 'R&A'),
    ('CSBS', 'CSBS'),
    ('CYS', 'CYS'),
    
    # Variations
    ('AIML', 'AI&ML'),
    ('AI ML', 'AI&ML'),
    ('AI-ML', 'AI&ML'),
    ('AI_ML', 'AI&ML'),
    ('ai&ml', 'AI&ML'),
    ('Ai&Ml', 'AI&ML'),
    
    ('AIDS', 'AI&DS'),
    ('AI DS', 'AI&DS'),
    ('AI-DS', 'AI&DS'),
    
    ('RA', 'R&A'),
    ('R A', 'R&A'),
    ('R-A', 'R&A'),
    
    # Invalid
    ('INVALID', None),
    ('XYZ', None),
]

print('\nDepartment Normalization Tests:')
print('=' * 70)

all_passed = True
for input_name, expected in test_cases:
    result = normalize_department_name(input_name)
    status = 'PASS' if result == expected else 'FAIL'
    if result != expected:
        all_passed = False
    print(f'{input_name:15} -> {str(result):10} (Expected: {str(expected):10}) {status}')

print('=' * 70)
if all_passed:
    print('\nOverall: ALL TESTS PASSED')
else:
    print('\nOverall: SOME TESTS FAILED')
