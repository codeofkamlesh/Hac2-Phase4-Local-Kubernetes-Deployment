---
id: "025"
title: "Update Deprecated Cohere Model Name"
stage: "general"
date_iso: "2026-02-03"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "main"
user: "kamlesh_kumar"
command: "/sp.implement"
labels: ["backend", "ai-model", "cohere", "api"]
spec: null
ticket: null
adr: null
pr: null
---

# Update Deprecated Cohere Model Name

## User Input
```
"Update Deprecated Cohere Model Name"; The backend is crashing with a 404 error from Cohere because the model `command-r-plus` has been deprecated and removed.

**REQUIRED FIX in `backend/main.py`:**

1.  **Update Model Name:**
    * Locate the `cohere_client.chat(...)` call inside `chat_endpoint`.
    * Change the model parameter from `model="command-r-plus"` to `model="command-r"`.
    * `command-r` is the current stable model that supports tool use.

**Goal:** Switch to a valid AI model so the API requests succeed.
```

## Response Text
Successfully updated the deprecated Cohere model name to fix the 404 error.

Changes made:
1. Updated the Cohere model in the chat endpoint:
   - Changed from: `model="command-r-plus"`
   - Changed to: `model="command-r"`

The `command-r` model is the current stable model that supports tool use, replacing the deprecated `command-r-plus` model. This resolves the 404 error from Cohere and allows API requests to succeed.

## Files Modified
 - /home/kamlesh_kumar/projects/Hac2-Phase3-AI-powered-todo-app-with-cahtbot/phase3/backend/main.py

## Outcome
The backend now uses a valid Cohere model, resolving the 404 error and allowing AI-powered chat functionality to work properly.