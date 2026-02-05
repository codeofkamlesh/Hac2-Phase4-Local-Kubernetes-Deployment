---
id: 43
title: "Fix Recurrence Logic Map Correct Column"
stage: general
date: "2026-02-04"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "main"
user: "kamlesh_kumar"
command: "manual"
labels: ["ai-chatbot", "recurrence-logic", "database-mapping", "parameter-normalization", "boolean-flag"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - "phase3/backend/models.py"
  - "phase3/backend/tools.py"
  - "phase3/backend/routes/tasks.py"
  - "phase3/backend/test_recurrence_fix_correct.py"
  - "phase3/backend/FINAL_RECURRENCE_FIX_SUMMARY.md"
tests:
  - "test_robust_tools.py"
  - "test_recurrence_fix.py"
  - "test_recurrence_fix_correct.py"
---

# Fix Recurrence Logic Map Correct Column

## Prompt Text
```
"Fix Recurrence Logic: Map to Correct Column & Set Boolean Flag" ; The user identified a database mismatch preventing recurring tasks from appearing on the frontend.
**Evidence from DB Screenshot:**
* **Working (Manual):** `recurring`=TRUE, `recurrencePattern`='weekly', `recurringInterval`=NULL.
* **Broken (Chatbot):** `recurring`=FALSE, `recurrencePattern`=NULL, `recurringInterval`='weekly'.

**OBJECTIVE:**
Force the `update_task` (and `add_task`) tools to write to `recurrencePattern` and explicitly set the `recurring` boolean to True.

**STEP 1: REWRITE `update_task` (in `backend/main.py` or `tools.py`):**

```python
def update_task(session: Session, user_id: str, task_id: int | str, updates: dict):
    # 1. Resolve ID (Keep existing logic)
    db_task_id = resolve_task_id(session, user_id, task_id)
    if not db_task_id:
        return f"Task '{task_id}' not found."

    task = session.get(Task, db_task_id)

    # 2. NORMALIZATION LOGIC (THE FIX)
    # Map all AI variations to the CORRECT column 'recurrencePattern'
    recurrence_keys = ['repeat', 'recurring', 'frequency', 'pattern', 'recurring_pattern', 'recurrence_pattern', 'recurringInterval', 'recurring_interval']

    new_pattern = None
    for key in recurrence_keys:
        if key in updates:
            new_pattern = updates.pop(key)
            break

    # If a pattern was found, Apply the FIX:
    if new_pattern:
        # A. Set the correct text column
        updates['recurrencePattern'] = new_pattern
        # B. CRITICAL: Set the boolean flag to True
        updates['recurring'] = True
        # C. Clear the incorrect column (optional cleanup)
        updates['recurringInterval'] = None

    # 3. Apply updates
    for key, value in updates.items():
        if hasattr(task, key):
            setattr(task, key, value)

    session.add(task)
    session.commit()
    session.refresh(task)
    return f"Task updated. Recurrence set to: {task.recurrencePattern} (Active: {task.recurring})"
```
```

## Response Summary
Successfully fixed the recurrence logic by updating the Task model to include proper recurring fields, updating the parameter mapping logic in update_task and add_task functions to map AI inputs to the correct database columns (recurrencePattern) and set the recurring boolean flag to True.

## Outcome & Impact
- Fixed database column mapping: AI inputs now map to recurrencePattern instead of recurringInterval
- Set recurring boolean flag to True when recurrence pattern exists
- Updated Task model to include proper recurring and recurrence_pattern fields
- Maintained backward compatibility for existing functionality
- All tests pass confirming the fix works correctly

## Tests Summary
- test_robust_tools.py: Verifies parameter mapping and ID resolution
- test_recurrence_fix.py: Confirms parameter normalization works
- test_recurrence_fix_correct.py: New verification script for the fix

## Files Summary
- phase3/backend/models.py: Added recurring boolean and recurrence_pattern fields
- phase3/backend/tools.py: Updated parameter mapping logic in update_task and add_task
- phase3/backend/routes/tasks.py: Fixed import path
- phase3/backend/test_recurrence_fix_correct.py: Verification script
- phase3/backend/FINAL_RECURRENCE_FIX_SUMMARY.md: Implementation summary

## Next Prompts
- Verify frontend displays recurring tasks correctly
- Test edge cases for recurrence patterns
- Add additional validation for recurrence values

## Reflection Note
The fix successfully addressed the database schema mismatch between what the frontend expects and what the backend was providing.

## Failure Modes Observed
None observed - all tests passed and functionality works as expected.

## Next Experiment to Improve Prompt Quality
Consider adding validation to ensure recurrence patterns match expected values before saving.