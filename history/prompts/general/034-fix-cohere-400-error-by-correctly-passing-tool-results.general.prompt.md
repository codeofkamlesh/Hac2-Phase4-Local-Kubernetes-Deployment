---
id: "034"
title: "Fix Cohere 400 Error by Correctly Passing Tool Results"
stage: "general"
date_iso: "2026-02-03"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "main"
user: "kamlesh_kumar"
command: "/sp.implement"
labels: ["backend", "cohere", "error-fix", "tool-results"]
spec: null
ticket: null
adr: null
pr: null
---

# Fix Cohere 400 Error by Correctly Passing Tool Results

## User Input
```
"Fix Cohere 400 Error by Correctly Passing Tool Results" ; The backend crashes with `400 Bad Request: message must be at least 1 token long or tool results must be specified`.
This happens in the multi-step loop because the subsequent calls to Cohere are sending an empty message WITHOUT correctly passing the `tool_results` list.

**REQUIRED REWRITE of `backend/main.py` -> `chat_endpoint`:**

Replace the entire `while` loop logic with this explicit state management:

1.  **Initialize Variables:**
    * `current_message = request.message`
    * `current_tool_results = None`

2.  **The Loop (`while True`):**
    * **Call Cohere:**
        ```python
        response = cohere_client.chat(
            message=current_message,
            chat_history=chat_history,
            tool_results=current_tool_results, # Pass results if they exist
            model="command-r-08-2024",
            tools=[...list of tools...],
            temperature=0.3
        )
        ```
    * **Check Output:**
        * If `response.tool_calls`:
            * 1. Print `f"🔧 Tools Triggered: {response.tool_calls}"`
            * 2. Execute tools and build the `tool_results` list strictly as: `{'call': tool_call, 'outputs': [{'result': output}]}`.
            * 3. **CRITICAL UPDATE:** Set `current_message = ""` (Empty string) AND `current_tool_results = tool_results`.
            * 4. `continue` (Loop back to send results).
        * Else:
            * Break loop (Final answer received).

**Goal:** Ensure that when `current_message` is empty, `tool_results` is populated, satisfying the API requirement.
```

## Response Text
Successfully fixed the Cohere 400 error by rewriting the multi-step loop logic to properly handle tool results.

Changes made:
1. **Initialized Variables:**
   - `current_message = request.message`
   - `current_tool_results = None`

2. **Implemented Proper Loop Logic:**
   - Added `tool_results=current_tool_results` parameter to the Cohere client call
   - When tool calls are detected, execute tools and build `tool_results` list in the required format: `{'call': tool_call, 'outputs': [{'result': output}]}`
   - After executing tools, set `current_message = ""` (empty string) and `current_tool_results = tool_results`
   - Continue the loop to send results back to the AI for next steps
   - When no tool calls exist, break the loop to return the final response

3. **Added Proper Error Handling:**
   - Maintained fallback logic for model errors
   - Preserved existing task guardrails and rate limiting
   - Added temperature parameter for consistent behavior

The backend now properly satisfies the Cohere API requirement that either a message must be at least 1 token long OR tool results must be specified. When `current_message` is empty, `tool_results` is populated with the executed tool results.

## Files Modified
 - /home/kamlesh_kumar/projects/Hac2-Phase3-AI-powered-todo-app-with-cahtbot/phase3/backend/main.py

## Outcome
The backend now properly handles multi-step tool execution without triggering the 400 Bad Request error, ensuring smooth AI interaction flow.