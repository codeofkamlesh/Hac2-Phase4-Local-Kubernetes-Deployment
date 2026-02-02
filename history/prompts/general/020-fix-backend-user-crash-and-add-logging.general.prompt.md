---
id: "020"
title: "Fix Backend User Crash and Add Logging"
stage: "general"
date_iso: "2026-02-03"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "main"
user: "kamlesh_kumar"
command: "/sp.implement"
labels: ["backend", "authentication", "foreign-key", "logging", "error-handling"]
spec: null
ticket: null
adr: null
pr: null
---

# Fix Backend User Crash and Add Logging

## User Input
```
Fix Backend User Crash and Add Logging The Frontend is now correctly sending the `user_id`, but the Backend returns a 500 Error.
This is caused by a **Foreign Key Violation**: The `user_id` exists in the Frontend (Better Auth) but NOT in the Backend (Neon DB `user` table).

**REQUIRED FIXES in `backend/main.py`:**

1.  **Handle New Users (Upsert Logic):**
    * Inside `chat_endpoint`, BEFORE creating a `Conversation` or `Message`:
    * Check if the user exists: `existing_user = session.get(User, request.user_id)`.
    * **If user does NOT exist:**
        * Create it: `new_user = User(id=request.user_id, email=f"{request.user_id}@placeholder.com", name="Guest User")`
        * `session.add(new_user)`
        * `session.commit()`
    * This ensures the Foreign Key constraint is satisfied.

2.  **Enable Error Logs:**
    * In the `except Exception as e:` block, ADD:
      `import traceback`
      `traceback.print_exc()`
      `print(f"❌ CRITICAL ERROR: {e}")`
    * This allows us to see the exact error in the terminal if it fails again.

**Goal:** Automatically sync the user to the Postgres DB when they start a chat, preventing the 500 Crash.
```

## Response Text
Successfully fixed the backend user crash caused by foreign key violations and added comprehensive error logging.

Changes made:
1. Added user upsert logic in the chat_endpoint function:
   - Check if user exists using `session.get(User, request.user_id)`
   - If user doesn't exist, create a new user with placeholder data
   - Added logging to confirm when new users are created
   - This ensures foreign key constraints are satisfied before creating conversations/messages

2. Enhanced error logging in the exception handler:
   - Added `import traceback` statement
   - Added `traceback.print_exc()` to show detailed stack traces
   - Added critical error logging with `print(f"❌ CRITICAL ERROR: {e}")`
   - This enables better debugging of future issues

The backend now automatically syncs users from the frontend authentication system to the backend database, preventing the 500 error crashes caused by foreign key violations.

## Files Modified
 - /home/kamlesh_kumar/projects/Hac2-Phase3-AI-powered-todo-app-with-cahtbot/phase3/backend/main.py

## Outcome
The backend now handles new users gracefully by automatically creating user records when they don't exist, preventing foreign key constraint violations. Comprehensive error logging has been added to aid in debugging future issues.