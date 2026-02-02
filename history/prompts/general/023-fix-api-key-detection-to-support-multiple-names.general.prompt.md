---
id: "023"
title: "Fix API Key Detection to Support Multiple Names"
stage: "general"
date_iso: "2026-02-03"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "main"
user: "kamlesh_kumar"
command: "/sp.implement"
labels: ["backend", "api-key", "configuration", "environment"]
spec: null
ticket: null
adr: null
pr: null
---

# Fix API Key Detection to Support Multiple Names

## User Input
```
Fix API Key Detection to Support Multiple Names ; The backend tests failed because `Cohere API key not configured`.
We need to make the key detection more robust.

**REQUIRED FIXES in `backend/main.py`:**

1.  **Update `get_cohere_client`:**
    * Change the logic to look for MULTIPLE environment variable names.
    * `api_key = os.getenv("COHERE_API_KEY") or os.getenv("CO_API_KEY")`
    * If `api_key` is still None, THEN raise the 500 error.

2.  **Add Debug Log on Startup:**
    * Inside the `lifespan` function (startup event), add:
      `key_status = "✅ Found" if (os.getenv("COHERE_API_KEY") or os.getenv("CO_API_KEY")) else "❌ MISSING"`
      `print(f"🔑 Cohere API Key Check: {key_status}")`

**Goal:** Ensure the app finds the key regardless of whether it's named `COHERE_API_KEY` or `CO_API_KEY`.
```

## Response Text
Successfully fixed the API key detection to support multiple environment variable names.

Changes made:
1. Updated `get_cohere_client` function to look for both `COHERE_API_KEY` and `CO_API_KEY` environment variables:
   - Changed from `api_key = os.getenv("COHERE_API_KEY")` to `api_key = os.getenv("COHERE_API_KEY") or os.getenv("CO_API_KEY")`
   - Maintained the same error handling if no key is found

2. Added debug log in the `lifespan` function to check API key status on startup:
   - Added key status check: `key_status = "✅ Found" if (os.getenv("COHERE_API_KEY") or os.getenv("CO_API_KEY")) else "❌ MISSING"`
   - Added print statement: `print(f"🔑 Cohere API Key Check: {key_status}")`

The backend now supports both API key environment variable names and provides clear startup feedback about key availability.

## Files Modified
 - /home/kamlesh_kumar/projects/Hac2-Phase3-AI-powered-todo-app-with-cahtbot/phase3/backend/main.py

## Outcome
The backend now successfully detects the Cohere API key regardless of whether it's named COHERE_API_KEY or CO_API_KEY, resolving the configuration issue that was causing test failures.