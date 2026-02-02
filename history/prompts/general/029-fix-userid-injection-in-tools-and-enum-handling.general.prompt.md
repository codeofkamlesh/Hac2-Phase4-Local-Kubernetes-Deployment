---
id: "029"
title: "Fix UserID Injection in Tools and Enum Handling"
stage: "general"
date_iso: "2026-02-03"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "main"
user: "kamlesh_kumar"
command: "/sp.implement"
labels: ["backend", "user-id", "enums", "error-fix"]
spec: null
ticket: null
adr: null
pr: null
---

# Fix UserID Injection in Tools and Enum Handling

## User Input
```
"Fix UserID Injection in Tools and Enum Handling" ; The backend is failing with two specific errors:
1. `psycopg2.errors.ForeignKeyViolation`: `add_task` receives an empty `userId`.
2. `AttributeError: 'str' object has no attribute 'value'`: occurring in conversation history and tool outputs.

**REQUIRED FIXES:**

1.  **Update `backend/main.py` (Inject User ID):**
    * Locate the loop where `response.tool_calls` are processed.
    * **CRITICAL FIX:** Before calling `add_task`, `list_tasks`, etc., **FORCE INJECT** the `user_id`.
    * *Code Example:*
        ```python
        if tool_name == "add_task":
            tool_parameters["user_id"] = request.user_id  # <--- Inject this!
            result = add_task(session, **tool_parameters)
        elif tool_name == "list_tasks":
            tool_parameters["user_id"] = request.user_id  # <--- Inject this!
            result = list_tasks(session, **tool_parameters)
        ```

2.  **Update `backend/main.py` (Fix Enum Error in History):**
    * Locate the `get_conversation_history` loop.
    * Change `msg.role.value` to just `msg.role`.
    * *Logic:* SQLModel often returns the value directly as a string. Accessing `.value` on a string causes the crash.

3.  **Update `backend/tools.py` (Fix Enum Error in Tools):**
    * In `add_task`, ensure `priority` is handled as a string. If it's an Enum, convert it: `priority = priority.value if hasattr(priority, 'value') else priority`.

**Goal:** Ensure `add_task` gets the correct `user_id` and remove all `.value` calls that are crashing on strings.
```

## Response Text
Successfully fixed UserID injection and enum handling errors.

Changes made:

1. **UserID Injection in main.py:**
   - Updated tool processing loop to inject `user_id` into all tool calls
   - Added: `tool_parameters["user_id"] = request.user_id` for all tool calls (add_task, list_tasks, complete_task, delete_task, update_task)
   - Fixed ForeignKeyViolation by ensuring user_id is passed to all tools

2. **Enum Error Fix in tools.py:**
   - Updated `get_conversation_history` to use `msg.role` instead of `msg.role.value`
   - Updated `add_task` to accept user_id parameter and handle priority enum conversion
   - Updated `list_tasks` to accept user_id parameter and filter by user
   - Updated `complete_task` to accept user_id parameter and verify task ownership
   - Updated `delete_task` to accept user_id parameter and verify task ownership
   - Updated `update_task` to accept user_id parameter and handle priority enum conversion
   - Added safe enum access: `priority.value if hasattr(priority, 'value') else priority`

3. **Safe Enum Handling:**
   - Added defensive code to handle both string and enum values
   - Used `hasattr(obj, 'value')` checks before accessing `.value` attribute
   - Fixed AttributeError by checking if value is already a string

The backend now properly injects user_id into all tool calls and handles enums safely without crashes.

## Files Modified
 - /home/kamlesh_kumar/projects/Hac2-Phase3-AI-powered-todo-app-with-cahtbot/phase3/backend/main.py
 - /home/kamlesh_kumar/projects/Hac2-Phase3-AI-powered-todo-app-with-cahtbot/phase3/backend/tools.py

## Outcome
The backend now properly injects user_id into all tool calls, preventing ForeignKeyViolation errors, and handles enum values safely without AttributeError crashes.