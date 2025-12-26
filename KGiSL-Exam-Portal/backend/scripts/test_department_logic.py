from exams.utils import get_department_from_register_no

# Test cases: (register_number, expected_department)
test_cases = [
    ('711725UAM132', 'AI&ML'),
    ('711724UAD217', 'AI&DS'),
    ('711623UCS089', 'CSE'),
    ('711726UEC210', 'ECE'),
    ('711725UIT001', 'IT'),
    ('711725UME050', 'MECH'),
    ('711725URA100', 'R&A'),
    ('711725UCB200', 'CSBS'),
    ('711725UCY300', 'CYS'),
    ('711725XXX999', None),  # Invalid department code
]

print('\nDepartment Identification Tests:')
print('=' * 70)

all_passed = True
for register_no, expected in test_cases:
    result = get_department_from_register_no(register_no)
    status = 'PASS' if result == expected else 'FAIL'
    if result != expected:
        all_passed = False
    print(f'{register_no:15} -> {str(result):10} (Expected: {str(expected):10}) {status}')

print('=' * 70)
if all_passed:
    print('\nOverall: ALL TESTS PASSED')
else:
    print('\nOverall: SOME TESTS FAILED')
