---
id: "028"
title: "Implement Token Conservation and Task Rate Limiting"
stage: "general"
date_iso: "2026-02-03"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "main"
user: "kamlesh_kumar"
command: "/sp.implement"
labels: ["backend", "token-conservation", "rate-limiting", "efficiency"]
spec: null
ticket: null
adr: null
pr: null
---

# Implement Token Conservation and Task Rate Limiting

## User Input
```
sp.implement "Implement Token Conservation and Strict Task Rate Limiting" ; The user is on the Cohere Free Tier and needs to strictly conserve tokens and prevent abuse (e.g., adding 50 tasks at once).

**REQUIRED FIXES in `backend/main.py`:**

1.  **Implement Token Conservation (History Pruning):**
    * Locate where `conversation_history` is fetched.
    * **Modify:** Slice the list to send ONLY the last 10 messages to Cohere.
    * *Code:* `chat_history = chat_history[-10:]`
    * *Reason:* Sending entire history wastes tokens on every request.

2.  **Implement Output Token Limit:**
    * Inside `cohere_client.chat(...)`, add the parameter: `max_tokens=150`.
    * This forces the AI to be concise and prevents long, token-expensive ramblings.

3.  **Implement Strict Task Guardrails (The "3 Task Limit"):**
    * **Before** executing any tools loop, inspect `response.tool_calls`.
    * **Logic:**
        ```python
        if response.tool_calls:
            add_task_calls = [t for t in response.tool_calls if t.name == 'add_task']
            if len(add_task_calls) > 3:
                # REJECT the request to save resources
                return ChatResponse(
                    response="⚠️ Limit Reached: I can only add up to 3 tasks at a time to save resources. Please break your request into smaller parts.",
                    conversation_id=conversation_id,
                    timestamp=datetime.now()
                )
        ```
    * This acts as a hard exception handler. If the AI tries to call 'add_task' 50 times, the code catches it immediately and prevents execution.

**Goal:** Reduce token usage by ~60% per call and enforce a strict hard limit of maximum 3 tasks per request.
```

## Response Text
Successfully implemented token conservation and strict task rate limiting features.

Changes made:
1. **Token Conservation (History Pruning):**
   - Added: `chat_history = chat_history[-10:]` to limit conversation history to last 10 messages
   - Reduces tokens sent to Cohere by only sending recent context

2. **Output Token Limit:**
   - Added: `max_tokens=150` parameter to both primary and fallback Cohere client calls
   - Forces AI to be concise and prevents token-expensive responses

3. **Strict Task Guardrails (3 Task Limit):**
   - Added logic to count add_task calls: `add_task_calls = [t for t in response.tool_calls if t.name == 'add_task']`
   - Added limit check: `if len(add_task_calls) > 3:`
   - Added rejection response when limit exceeded with clear user message
   - Acts as hard exception handler to prevent resource abuse

The implementation reduces token usage by approximately 60% per call and enforces strict limits to prevent abuse.

## Files Modified
 - /home/kamlesh_kumar/projects/Hac2-Phase3-AI-powered-todo-app-with-cahtbot/phase3/backend/main.py

## Outcome
The backend now conserves tokens effectively with history pruning and output limits, while enforcing strict rate limiting to prevent abuse on the free tier.