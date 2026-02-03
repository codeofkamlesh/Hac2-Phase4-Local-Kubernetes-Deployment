---
id: 036
title: "phase-5-ultimate-backend-stability"
stage: "red"
date_iso: "2026-02-03"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "general"
branch: "main"
user: "kamlesh_kumar"
command: "sp.implement"
labels: ["backend", "stability", "cohere", "chat-history", "schema-enforcement", "react-loop"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - "/home/kamlesh_kumar/projects/Hac2-Phase3-AI-powered-todo-app-with-cahtbot/phase3/backend/main.py"
tests_yaml:
  - "/home/kamlesh_kumar/projects/Hac2-Phase3-AI-powered-todo-app-with-cahtbot/phase3/backend/test_updated_sanitization.py"
prompt_text: |
  "Phase 5: Ultimate Backend Stability & Schema Enforcement" , The backend is facing persistent 400 Errors from Cohere (`all elements in history must have a message`) and loop crashes. The user also requires strict adherence to the existing database schema.

  **REQUIRED REWRITE of `backend/main.py` -> `chat_endpoint`:**

  **1. Define the System Preamble (Schema Enforcement):**
     * Create a constant string `SYSTEM_PREAMBLE` at the top of the file.
     * Content: "You are a helpful Task Assistant. You operate on a Postgres Database with these exact tables: 'User', 'Task' (columns: id, title, description, priority, completed, dueDate, userId), 'Conversation', 'Message'. DO NOT hallicinate new columns. When adding tasks, strictly use the defined tools. Be concise."

  **2. Sanitize History (The Critical Fix):**
     * Inside `chat_endpoint`, after fetching `chat_history` from DB:
     * **Force Convert None to String:**
       ```python
       sanitized_history = []
       for msg in chat_history:
           content = msg.get("message")
           if content is None:
               content = "" # Fixes the 400 Error
           sanitized_history.append({"role": msg["role"], "message": content})
       ```

  **3. Implement the Robust Re-Act Loop:**
     * Initialize `current_message = request.message`.
     * Initialize `current_tool_results = None`.
     * Start `while True` loop (max 10 turns):
       * **Call Cohere:**
         * Pass `preamble=SYSTEM_PREAMBLE`.
         * Pass `chat_history=sanitized_history`.
         * Pass `message=current_message`.
         * Pass `tool_results=current_tool_results`.
       * **Handle Response:**
         * If `response.tool_calls`:
           * Execute tools (Inject `user_id` strictly).
           * Append Tool Inputs to `sanitized_history` (role='USER', message='').
           * Build `tool_results` list.
           * **CRITICAL:** Set `current_message = ""` and `current_tool_results = tool_results` for the next turn.
           * `continue`
         * If `response.text`:
           * Save response to DB.
           * Return response to frontend.
           * `break`

  **Goal:** A crash-proof endpoint that cleans data before sending to AI and strictly follows the loop logic without dropping parameters.
response_text: |
  Successfully implemented the ultimate backend stability and schema enforcement rewrite. The changes made:

  1. Added SYSTEM_PREAMBLE constant at the top of main.py with schema enforcement:
     - Specifies exact database tables and columns
     - Prevents hallucination of new columns
     - Enforces use of defined tools

  2. Implemented robust sanitization in chat_endpoint:
     - Creates sanitized_history from conversation history
     - Converts None values to empty strings to prevent 400 errors
     - Maintains role information while sanitizing message content

  3. Rewrote the Re-Act loop with crash-proof design:
     - Initializes current_message and current_tool_results properly
     - Passes preamble, sanitized_history, message, and tool_results to Cohere
     - Handles tool calls with strict user_id injection
     - Properly manages turn transitions with empty message and tool results
     - Saves responses to database and returns to frontend

  The implementation ensures schema adherence, prevents NoneType errors, and creates a stable loop that handles both tool calls and text responses reliably.
outcome: "Implemented crash-proof chat endpoint with schema enforcement and robust sanitization"
evaluation: "The implementation successfully resolves the reported issues. Backend should now be stable with proper schema enforcement and no more 400 errors from Cohere."
---

# Phase 5: Ultimate Backend Stability & Schema Enforcement

## Summary
Implemented comprehensive rewrite of the chat endpoint to achieve ultimate backend stability with schema enforcement, fixing persistent 400 errors from Cohere and loop crashes.

## Changes Made

### 1. Added System Preamble for Schema Enforcement
Defined `SYSTEM_PREAMBLE` constant at the top of main.py:
```python
SYSTEM_PREAMBLE = "You are a helpful Task Assistant. You operate on a Postgres Database with these exact tables: 'User', 'Task' (columns: id, title, description, priority, completed, dueDate, userId), 'Conversation', 'Message'. DO NOT hallicinate new columns. When adding tasks, strictly use the defined tools. Be concise."
```

### 2. Implemented Robust History Sanitization
In the chat endpoint, replaced the old sanitization with the required approach:
```python
sanitized_history = []
for msg in conversation_history:
    content = msg.get("content")
    if content is None:
        content = "" # Fixes the 400 Error
    sanitized_history.append({"role": msg["role"], "message": content})
```

### 3. Rewrote the Re-Act Loop
Completely rewrote the chat loop with crash-proof design:
- Proper initialization of `current_message` and `current_tool_results`
- Passes preamble, sanitized_history, message, and tool_results to Cohere
- Handles tool calls with strict user_id injection in all tools
- Proper turn management with empty message and tool results
- Reliable response saving and return mechanism

## Files Modified
- `phase3/backend/main.py` - Complete rewrite of chat endpoint
- `phase3/backend/test_updated_sanitization.py` - Verification tests

## Verification
Created and ran tests that confirm the new implementation works correctly with proper sanitization, schema enforcement, and robust loop handling.