---
id: "031"
title: "Implement Multi-Step Tool Execution Loop"
stage: "general"
date_iso: "2026-02-03"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "main"
user: "kamlesh_kumar"
command: "/sp.implement"
labels: ["backend", "ai", "tools", "loop", "multi-step"]
spec: null
ticket: null
adr: null
pr: null
---

# Implement Multi-Step Tool Execution Loop

## User Input
```
"Implement Multi-Step Tool Execution Loop" ; The AI currently stops after executing a single tool (e.g., it runs `list_tasks` to find an ID but never follows up with `update_task`).
We need to implement a **Re-Act (Reason + Act) Loop** in the backend.

**REQUIRED REWRITE of `backend/main.py` (`chat_endpoint`):**

1.  **Implement `while` Loop:**
    * Wrap the `cohere_client.chat(...)` call inside a `while True:` loop.
    * **Max Turns:** Add a safety counter (e.g., `limit=5`) to prevent infinite loops.

2.  **Loop Logic:**
    * **Call Cohere:** Get `response`.
    * **If `response.tool_calls` exists:**
        * 1. Execute the tools (using the existing logic with `user_id` injection).
        * 2. Append the tool results to `chat_history` (formatted strictly as Cohere expects for tool outputs).
        * 3. **CONTINUE** the loop (Send the new history back to Cohere so it can determine the NEXT step).
    * **If `response.text` exists (and no tool calls):**
        * BREAK the loop and return the final text to the user.

3.  **Chat History Management:**
    * Ensure that intermediate tool results are stored in the local `chat_history` list passed to `cohere.chat`, so the model has "memory" of what it just did.

**Goal:** Enable the AI to perform multi-step actions like "Find task X (Step 1) AND THEN Update it (Step 2)" in a single user request.
```

## Response Text
Successfully implemented multi-step tool execution loop (Re-Act: Reason + Act).

Changes made:
1. **Implemented While Loop:**
   - Wrapped Cohere client call in `while turn_count < max_turns:` loop
   - Added safety counter with `max_turns = 5` to prevent infinite loops
   - Added turn counter to track execution progress

2. **Loop Logic:**
   - Check for `response.tool_calls` existence
   - Execute tools with user_id injection (preserving existing logic)
   - Append tool results to `chat_history` with role "TOOL"
   - Add tool results to AI response
   - Continue loop to allow AI to determine next steps
   - Break loop when no tool calls and text response exists

3. **Chat History Management:**
   - Maintain local `chat_history` list with tool results
   - Format tool results as Cohere expects for tool outputs
   - Add original user message to chat history
   - Allow AI to have "memory" of previous actions

4. **Safety Features:**
   - Max turn limit to prevent infinite loops
   - Warning message when max turns reached
   - Preserved existing task guardrails and error handling

The AI can now perform multi-step actions like "Find task X (Step 1) AND THEN Update it (Step 2)" in a single user request.

## Files Modified
 - /home/kamlesh_kumar/projects/Hac2-Phase3-AI-powered-todo-app-with-cahtbot/phase3/backend/main.py

## Outcome
The backend now supports multi-step tool execution, enabling the AI to perform sequential actions in a single request with proper memory of previous steps.