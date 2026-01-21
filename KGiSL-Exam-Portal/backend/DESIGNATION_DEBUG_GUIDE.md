# Designation Validation Debug Guide

## Overview
This document explains the designation validation flow and how to debug designation mismatch errors.

### Quick Triage Checklist
1. Reproduce the API call from the UI and confirm the designation the browser sends.
2. Tail the backend logs to ensure normalization kicks in and note the canonical output.
3. Spot-check the Excel sheet for any values that are not in the supported mapping table.
4. Re-run `debug_designation_flow.py` to validate the fix before retrying the allocation UI flow.

## Current Implementation

### Designation Flow: UI → Backend → Validation

```
Frontend UI
    ↓ sends
"Assistant Professor" or "Associate Professor"
    ↓
AdminFacultyAllocationView.post()
    ↓ logs
[FACULTY ALLOCATION] Designation from UI: 'Assistant Professor'
    ↓ calls
run_faculty_allocation()
    ↓ logs
[ALLOCATION] Received designation parameter: 'Assistant Professor'
    ↓ normalizes
normalize_designation()
    ↓ logs
[DESIGNATION] Raw input: 'Assistant Professor' (type: str)
[DESIGNATION] After normalization: 'ASSISTANT PROFESSOR'
[DESIGNATION] Validation SUCCESS: 'Assistant Professor' → 'ASSISTANT_PROFESSOR'
    ↓
Validates against: ['ASSISTANT_PROFESSOR', 'ASSOCIATE_PROFESSOR']
    ↓
Filters Excel data using normalized designation
    ↓ logs
[ALLOCATION] Excel designations found: ['ASST.PROF', 'ASSO.PROF', etc.]
[ALLOCATION] Normalizing Excel designations for filtering...
[ALLOCATION] After normalization: ['ASSISTANT_PROFESSOR', 'ASSOCIATE_PROFESSOR']
```

## Supported Designation Mappings

| Input (Excel/UI) | Normalized Output | Status |
|-----------------|-------------------|--------|
| "Assistant Professor" | ASSISTANT_PROFESSOR | ✓ Valid |
| "ASSISTANT PROFESSOR" | ASSISTANT_PROFESSOR | ✓ Valid |
| "Asst.Prof" | ASSISTANT_PROFESSOR | ✓ Valid |
| "ASST.PROF" | ASSISTANT_PROFESSOR | ✓ Valid |
| "Asst Prof" | ASSISTANT_PROFESSOR | ✓ Valid |
| "TEACHING ASSISTANT" | ASSISTANT_PROFESSOR | ✓ Valid |
| "Associate Professor" | ASSOCIATE_PROFESSOR | ✓ Valid |
| "ASSOCIATE PROFESSOR" | ASSOCIATE_PROFESSOR | ✓ Valid |
| "Asso.Prof" | ASSOCIATE_PROFESSOR | ✓ Valid |
| "ASSO.PROF" | ASSOCIATE_PROFESSOR | ✓ Valid |
| "Asso Prof" | ASSOCIATE_PROFESSOR | ✓ Valid |
| "PROFESSOR" | N/A | ✗ REJECTED |
| "Lecturer" | N/A | ✗ REJECTED |

## Debug Logging

### Enabled Loggers
- `apps.faculty.utils` - Logs designation normalization and allocation logic
- `apps.faculty.views` - Logs API requests and responses

### Log Format
```
{levelname} {timestamp} {module} {message}
```

### Example Log Output

#### Success Case (Assistant Professor):
```
INFO 2026-01-13 11:57:20,178 utils [DESIGNATION] Raw input: 'Assistant Professor' (type: str)
INFO 2026-01-13 11:57:20,179 utils [DESIGNATION] After normalization: 'ASSISTANT PROFESSOR'
INFO 2026-01-13 11:57:20,179 utils [DESIGNATION] Validation SUCCESS: 'Assistant Professor' → 'ASSISTANT_PROFESSOR'
INFO 2026-01-13 11:57:20,211 views [FACULTY ALLOCATION] Designation from UI: 'Assistant Professor'
INFO 2026-01-13 11:57:20,212 utils [ALLOCATION] Received designation parameter: 'Assistant Professor'
INFO 2026-01-13 11:57:20,213 utils [ALLOCATION] Normalized designation: 'ASSISTANT_PROFESSOR'
INFO 2026-01-13 11:57:20,214 utils [ALLOCATION] Designation validation PASSED
```

#### Failure Case (Invalid PROFESSOR):
```
INFO 2026-01-13 11:57:20,213 utils [DESIGNATION] Raw input: 'PROFESSOR' (type: str)
INFO 2026-01-13 11:57:20,213 utils [DESIGNATION] After normalization: 'PROFESSOR'
ERROR 2026-01-13 11:57:20,213 utils [DESIGNATION] Validation FAILED: 'PROFESSOR' not in allowed mapping
ERROR 2026-01-13 11:57:20,213 utils [DESIGNATION] Allowed values: ['ASSISTANT PROFESSOR', 'ASST.PROF', 'ASST PROF', 'TEACHING ASSISTANT', 'ASSOCIATE PROFESSOR', 'ASSO.PROF', 'ASSO PROF']
```

## Troubleshooting Steps

### Error: "Invalid designation: PROFESSOR"

**Root Cause:** Excel dataset contains rows with designation value "PROFESSOR"

**Solution:**
1. Check the Excel file at: `D:\AFS\FACULTY_DATASET(MODIFIED).xlsx`
2. Search for rows with designation = "PROFESSOR"
3. Update to one of the valid variants:
   - Change to "ASST.PROF" for Assistant Professors
   - Change to "ASSO.PROF" for Associate Professors

**How to verify:**
```bash
cd backend
python debug_designation_flow.py
```

### Error: "Invalid designation: TEACHING ASSISTANT"

**Status:** This should now work correctly (maps to ASSISTANT_PROFESSOR)

**If still failing:**
1. Check terminal logs for the exact input value
2. Look for hidden characters or extra whitespace
3. Verify normalization is being applied

### Error: UI selection not recognized

**Debug Steps:**
1. Open browser DevTools → Network tab
2. Make a faculty allocation request
3. Check the request payload for the `designation` field
4. Compare with what appears in terminal logs:
   ```
   [FACULTY ALLOCATION] Designation from UI: '...'
   ```
5. If they don't match, there's a frontend issue

## Testing Commands

### Test normalization function:
```bash
cd backend
python test_designation_normalization.py
```
Expected output: `22 passed, 0 failed`

### Test integration flow:
```bash
cd backend
python test_designation_integration.py
```
Expected output: `All integration tests passed!`

### Test with live logging:
```bash
cd backend
python debug_designation_flow.py
```

### Monitor real-time logs:
1. Start the backend server: `python manage.py runserver`
2. Make a faculty allocation request from the UI
3. Watch the terminal for log output showing:
   - What designation the UI sent
   - How it was normalized
   - Whether validation passed or failed

## Excel Dataset Validation

### Check for invalid designations in Excel:
```python
import pandas as pd
df = pd.read_excel(r"D:\AFS\FACULTY_DATASET(MODIFIED).xlsx", sheet_name='CSE')
print(df['DESIGNATION'].unique())
```

Expected output should only contain:
- ASST.PROF
- ASSO.PROF
- Assistant Professor
- Associate Professor
- TEACHING ASSISTANT

**NOT:**
- PROFESSOR
- Lecturer
- Senior Professor

## Common Issues

### Issue 1: Case Sensitivity
**Symptoms:** "Assistant professor" (lowercase 'p') fails
**Fix:** Already handled - normalization converts to uppercase

### Issue 2: Whitespace
**Symptoms:** "Assistant Professor " (trailing space) fails
**Fix:** Already handled - `.strip()` removes whitespace

### Issue 3: Excel Format Variants
**Symptoms:** Different sheets use different formats
**Fix:** Already handled - all variants mapped to canonical format

### Issue 4: Missing Logging
**Symptoms:** Can't see what's being validated
**Fix:** Logging is now enabled in `backend/settings.py`

## Files Modified

1. `backend/apps/faculty/utils.py` - Added logging to `normalize_designation()`
2. `backend/apps/faculty/views.py` - Added logging to `AdminFacultyAllocationView`
3. `backend/backend/settings.py` - Added LOGGING configuration
4. `backend/debug_designation_flow.py` - Debug script
5. `backend/test_designation_normalization.py` - Unit tests
6. `backend/test_designation_integration.py` - Integration tests

## Quick Reference

### Valid UI Values
- "Assistant Professor"
- "Associate Professor"

### Valid Excel Values
- "ASST.PROF"
- "ASSO.PROF"
- "Assistant Professor"
- "Associate Professor"
- "TEACHING ASSISTANT"

### Invalid Values (Will be Rejected)
- "PROFESSOR"
- "Lecturer"
- Any other variant

## Support

If errors persist after following this guide:
1. Run `python debug_designation_flow.py` to verify normalization
2. Check terminal logs for exact error messages
3. Verify Excel file doesn't contain invalid designations
4. Check browser network tab for actual API payload
