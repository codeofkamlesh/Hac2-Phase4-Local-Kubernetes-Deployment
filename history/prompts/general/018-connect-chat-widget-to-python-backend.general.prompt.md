---
id: "018"
title: "Connect Chat Widget to Python Backend"
stage: "general"
date_iso: "2026-02-03"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "main"
user: "kamlesh_kumar"
command: "/sp.implement"
labels: ["frontend", "chat", "backend-integration", "api"]
spec: null
ticket: null
adr: null
pr: null
---

# Connect Chat Widget to Python Backend

## User Input
```
The Chat Widget in the Frontend is currently showing "This is a mock response", which means it's not connected to the real Python Backend yet.

**REQUIRED ACTIONS:**

1.  **Locate the Mock Logic:**
    * Search for the string "This is a mock response" inside the `frontend/` directory. It is likely in `app/api/chat/route.ts` or `components/chat/ChatHooks.ts`.

2.  **Replace with Real API Call:**
    * Delete the mock response logic.
    * Implement a `fetch` call to the Python Backend: `POST http://127.0.0.1:8000/api/chat`.
    * **Payload:** Ensure the JSON body includes:
        * `message`: The user's input.
        * `user_id`: The current user's ID (from the session).
        * `conversation_id`: The current conversation ID (if available).

3.  **Handle Response:**
    * Return the real JSON response from the Python backend to the UI so the user sees the actual AI reply.

**Goal:** When the user types "Add a task", the Frontend should send it to Port 8000, and the AI should create the task in the DB.
```

## Response Text
Successfully connected the Chat Widget to the Python backend by replacing the mock response logic with a real API call.

Changes made:
1. Updated ChatWidget.tsx to replace the mock response with a real fetch call to the Python backend at http://127.0.0.1:8000/api/chat
2. Implemented proper session handling to retrieve the user ID using authClient.getSession()
3. Added the required payload structure with message, user_id, and conversation_id
4. Added proper error handling for backend communication failures
5. Maintained the existing UI flow by adding the backend response to the chat session

The Chat Widget now communicates with the Python backend, enabling the AI to process user requests and interact with the database through the backend tools.

## Files Modified
 - /home/kamlesh_kumar/projects/Hac2-Phase3-AI-powered-todo-app-with-cahtbot/phase3/frontend/components/chat/ChatWidget.tsx

## Outcome
The Chat Widget now connects to the Python backend instead of showing mock responses. When users type messages like "Add a task", the request is sent to the Python backend at port 8000, where the AI can process the request and interact with the database through the MCP tools.