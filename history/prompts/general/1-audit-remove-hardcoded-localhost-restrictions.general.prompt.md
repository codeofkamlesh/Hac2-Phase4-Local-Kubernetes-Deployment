---
id: 1
title: "audit-remove-hardcoded-localhost-restrictions"
stage: "general"
date_iso: "2026-02-05"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "main"
user: "kamlesh_kumar"
command: "/sp.implement \"Audit and Remove Hardcoded Localhost Restrictions\""
labels: ["deployment", "configuration", "security"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files_yaml:
  - "/home/kamlesh_kumar/projects/Hac2-Phase3-AI-powered-todo-app-with-cahtbot/phase3/frontend/components/chat/ChatWidget.tsx"
  - "/home/kamlesh_kumar/projects/Hac2-Phase3-AI-powered-todo-app-with-cahtbot/phase3/frontend/next.config.js"
tests_yaml: []
---

# Audit and Remove Hardcoded Localhost Restrictions

## Prompt Text
"Audit and Remove Hardcoded Localhost Restrictions" ; **OBJECTIVE:**
Scan the entire Frontend codebase to identify and remove any "Strict Rules", hardcoded fallbacks, or configuration overrides that are forcing the application to use `http://127.0.0.1:8000` or `localhost` instead of the environment variables.

**MY HF LINK:** https://kamlesh-todo-backend.hf.space

**INSTRUCTIONS:**

1.  **AUDIT `next.config.mjs` (CRITICAL):**
    * Check if there are any `rewrites()` or `async redirects()` that map `/api/:path*` to `http://127.0.0.1:8000`.
    * **FIX:** If found, comment them out OR update the destination to use `process.env.NEXT_PUBLIC_API_URL`.

2.  **AUDIT API UTILITIES:**
    * Search for any code pattern like: `const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000"`.
    * **FIX:** Change the fallback to the HF Link provided above, or remove the fallback entirely to force reliance on the Env Var.
    * Check `app/dashboard/components/ChatWidget.tsx` (and any other component making fetch calls) to ensure it is NOT ignoring the env var.

3.  **AUDIT MIDDLEWARE:**
    * Check `middleware.ts` (if it exists) for any logic blocking non-localhost origins.

4.  **ACTION:**
    * Replace any found instance of `http://127.0.0.1:8000` or `localhost:8000` with `https://kamlesh-todo-backend.hf.space` (or the env variable code).
    * Ensure the production build prefers the Vercel Environment Variable over any local default.

**CONSTRAINT:**
* Focus on fixing the "Deployment" issue.
* Do not break the logic, just update the target URLs.

## Response Text
Successfully audited and removed hardcoded localhost restrictions from the frontend codebase.

Key findings and changes:
1. Checked `next.config.js` - No hardcoded localhost configurations or rewrites found.
2. Found hardcoded localhost URL in `components/chat/ChatWidget.tsx:71`:
   - Original: `fetch('http://127.0.0.1:8000/api/chat', ...)`
   - Updated to use environment variable: `fetch(`${apiUrl}/api/chat', ...)` where `apiUrl = process.env.NEXT_PUBLIC_API_URL || 'https://kamlesh-todo-backend.hf.space'`
3. Verified `.env.local` already contains correct `NEXT_PUBLIC_API_URL` environment variable
4. No middleware file found in frontend that would block non-localhost origins
5. Confirmed no other hardcoded localhost URLs remain in source files

The application now properly uses the environment variable for API calls while maintaining a fallback to the Hugging Face space URL.

## Outcome
Hardcoded localhost restriction removed from ChatWidget component. The application will now properly use environment variables for API calls in deployment while maintaining the provided Hugging Face backend URL as fallback.

## Evaluation
Changes successfully applied. Application will now connect to the Hugging Face deployment backend instead of attempting to connect to localhost when deployed.