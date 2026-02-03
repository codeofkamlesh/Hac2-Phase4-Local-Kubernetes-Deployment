---
id: 037
title: "phase-5-ultimate-backend-stability-force-sanitize"
stage: "red"
date_iso: "2026-02-03"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "general"
branch: "main"
user: "kamlesh_kumar"
command: "sp.implement"
labels: ["backend", "stability", "cohere", "chat-history", "schema-enforcement", "sanitization", "react-loop"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - "/home/kamlesh_kumar/projects/Hac2-Phase3-AI-powered-todo-app-with-cahtbot/phase3/backend/main.py"
tests_yaml:
  - "/home/kamlesh_kumar/projects/Hac2-Phase3-AI-powered-todo-app-with-cahtbot/phase3/backend/test_phase5_fix.py"
prompt_text: |
  "Phase 5: Ultimate Backend Stability - Force Sanitize History & Strict Schema", The backend is failing with `400 Bad Request: all elements in history must have a message`.
  This is because `chat_history` fetched from the DB contains `None` values for tool outputs, which Cohere rejects.

  **REQUIRED REWRITE of `backend/main.py` -> `chat_endpoint`:**

  **1. Add System Preamble:**
     * Define `SYSTEM_PREAMBLE = "You are a Task Assistant. You operate on 'User', 'Task' (id, title, description, priority, completed, dueDate, userId), 'Conversation', 'Message' tables. DO NOT hallucinate columns. Use tools strictly."`

  **2. Implement Aggressive History Sanitization (The Fix):**
     * Inside `chat_endpoint`, REPLACE the history fetching block with this:
       ```python
       raw_history = get_conversation_history(session, conversation_id) if conversation_id else []
       sanitized_history = []
       for msg in raw_history:
           # CRITICAL: Force None to empty string
           content = msg.content if msg.content is not None else ""
           # Map 'assistant' role correctly if needed, otherwise keep as is
           sanitized_history.append({"role": msg.role, "message": content})
       ```

  **3. Robust Re-Act Loop Implementation:**
     * Initialize `current_message = request.message`.
     * Initialize `current_tool_results = None`.
     * **Loop (while True):**
       * **Call Cohere:**
         `response = cohere_client.chat(message=current_message, chat_history=sanitized_history, tool_results=current_tool_results, preamble=SYSTEM_PREAMBLE, ...)`
       * **If Tools Triggered:**
         * Execute tools (inject `user_id`).
         * **Append to History (Local Memory):**
           * Add User's tool invocation: `sanitized_history.append({"role": "USER", "message": ""})`
           * Add Assistant's tool plan: `sanitized_history.append({"role": "CHATBOT", "message": ""})` (or however Cohere expects it, usually just sending `tool_results` is enough for the next turn).
         * **Prepare Next Turn:**
           * `current_message = ""`
           * `current_tool_results = tool_results_list`
       * **If Text Response:**
         * Save to DB.
         * Return to User.
         * Break.

  **Goal:** Ensure that NO variable passed to `cohere_client.chat` ever contains `None` instead of a string.
response_text: |
  Successfully implemented the ultimate backend stability fix with aggressive history sanitization and strict schema enforcement. The changes made:

  1. Updated SYSTEM_PREAMBLE with strict schema enforcement:
     - Specifies exact database tables and columns
     - Prevents hallucination of new columns
     - Enforces use of tools strictly

  2. Implemented aggressive history sanitization:
     - Fetches raw history from get_conversation_history
     - Iterates through messages forcing None values to empty strings
     - Maps content to message while preserving roles
     - Prevents 400 errors from Cohere

  3. Rewrote the Re-Act loop with robust design:
     - Proper initialization of current_message and current_tool_results
     - Calls Cohere with preamble, sanitized_history, message, and tool_results
     - Handles tool calls with strict user_id injection
     - Appends proper history entries when tools are triggered
     - Manages turn transitions correctly
     - Saves responses to DB and returns to user

  The implementation ensures no None values are passed to Cohere, preventing the 400 Bad Request errors while maintaining all functionality.
outcome: "Implemented crash-proof chat endpoint with aggressive sanitization and strict schema enforcement"
evaluation: "The implementation successfully resolves the reported 400 Bad Request errors. Backend should now be stable with proper schema enforcement and no more None values passed to Cohere."
---

# Phase 5: Ultimate Backend Stability - Force Sanitize History & Strict Schema

## Summary
Implemented comprehensive fix for backend stability issues by adding aggressive history sanitization and strict schema enforcement to eliminate 400 Bad Request errors from Cohere.

## Changes Made

### 1. Updated System Preamble for Strict Schema Enforcement
Updated `SYSTEM_PREAMBLE` constant with stricter instructions:
```python
SYSTEM_PREAMBLE = "You are a Task Assistant. You operate on 'User', 'Task' (id, title, description, priority, completed, dueDate, userId), 'Conversation', 'Message' tables. DO NOT hallucinate columns. Use tools strictly."
```

### 2. Implemented Aggressive History Sanitization
Completely replaced the history sanitization logic with the required implementation:
```python
raw_history = get_conversation_history(conversation_id, session) if conversation_id else []

# Implement Aggressive History Sanitization (The Fix)
sanitized_history = []
for msg in raw_history:
    # CRITICAL: Force None to empty string
    content = msg["content"] if msg["content"] is not None else ""
    # Map 'assistant' role correctly if needed, otherwise keep as is
    sanitized_history.append({"role": msg["role"], "message": content})
```

### 3. Rewrote the Robust Re-Act Loop
Completely rewrote the chat loop with proper turn management:
- Proper initialization of `current_message` and `current_tool_results`
- Calls Cohere with all required parameters including preamble
- Handles tool calls with strict user_id injection in all tools
- Properly appends history entries when tools are triggered
- Adds both User and CHATBOT entries with empty messages when tools execute
- Correctly manages turn transitions with empty message and tool results
- Ensures reliable response saving and return mechanism

## Files Modified
- `phase3/backend/main.py` - Complete rewrite of chat endpoint sanitization and loop logic
- `phase3/backend/test_phase5_fix.py` - Verification tests

## Verification
Created and ran tests that confirm the new implementation works correctly with aggressive sanitization, strict schema enforcement, and robust loop handling that prevents None values from being passed to Cohere.