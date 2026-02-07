---
id: "001"
title: "Fix CORS Auth Issue"
stage: "general"
date_iso: "2026-02-06"
model: "claude-sonnet-4-5-20250929"
surface: "agent"
feature: "001-k8s-deployment"
branch: "main"
user: "kamlesh_kumar"
command: "/sp.implement **OBJECTIVE:** Fix the \"Network Error\" / CORS issue in the Frontend authentication. The application is running locally via Kubernetes/Docker (localhost:3000), but the Auth Client is incorrectly trying to send requests to the remote Vercel URL (\"https://hac2-phase4-local-kubernetes-deploy.vercel.app\"), which causes CORS blocks.\n\n**TASK:**\n1.  **SEARCH:** Scan the `frontend/` directory (specifically `frontend/lib/auth-client.ts` or `.env` files) for the string: \"hac2-phase4-local-kubernetes-deploy.vercel.app\".\n2.  **FIX:**\n    * If found in `auth-client.ts`: Change the `baseURL` to \"http://localhost:3000\" (or use `process.env.BETTER_AUTH_URL` if available).\n    * Ideally, set it to: `baseURL: process.env.NEXT_PUBLIC_app_url || \"http://localhost:3000\"` so it works in both places.\n    * If found in `.env` files: Ensure the local `.env` points to localhost.\n3.  **VERIFY:** Ensure that after the fix, the `createAuthClient` configuration uses the local address when running locally.\n\n**CONTEXT:**\nThe user is getting 204 No Content / CORS errors because the origin is 'localhost:3000' but the target host is the Vercel production deployment. We must force the app to talk to itself locally."
labels: ["cors", "authentication", "frontend", "local-development"]
link_spec: null
link_ticket: null
link_adr: null
link_pr: null
files_yaml: |
  - phase4/frontend/lib/auth-client.ts
  - phase4/frontend/.env.local
  - phase4/backend/main.py
tests_yaml: |
  - "Verify auth requests now target localhost:3000 instead of Vercel URL"
  - "Confirm CORS errors are resolved in browser console"
  - "Test that authentication flow works in local development"
prompt_text: "**OBJECTIVE:**\nFix the \"Network Error\" / CORS issue in the Frontend authentication. The application is running locally via Kubernetes/Docker (localhost:3000), but the Auth Client is incorrectly trying to send requests to the remote Vercel URL (\"https://hac2-phase4-local-kubernetes-deploy.vercel.app\"), which causes CORS blocks.\n\n**TASK:**\n1.  **SEARCH:** Scan the `frontend/` directory (specifically `frontend/lib/auth-client.ts` or `.env` files) for the string: \"hac2-phase4-local-kubernetes-deploy.vercel.app\".\n2.  **FIX:**\n    * If found in `auth-client.ts`: Change the `baseURL` to \"http://localhost:3000\" (or use `process.env.BETTER_AUTH_URL` if available).\n    * Ideally, set it to: `baseURL: process.env.NEXT_PUBLIC_app_url || \"http://localhost:3000\"` so it works in both places.\n    * If found in `.env` files: Ensure the local `.env` points to localhost.\n3.  **VERIFY:** Ensure that after the fix, the `createAuthClient` configuration uses the local address when running locally.\n\n**CONTEXT:**\nThe user is getting 204 No Content / CORS errors because the origin is 'localhost:3000' but the target host is the Vercel production deployment. We must force the app to talk to itself locally."
response_text: "Successfully fixed the CORS authentication issue by making the following changes:\n\n1. **Updated auth-client.ts** (`phase4/frontend/lib/auth-client.ts`):\n   - Changed to use environment variable with localhost fallback: `baseURL: process.env.NEXT_PUBLIC_AUTH_URL || \"http://localhost:3000\"`\n\n2. **Fixed environment variables** (`phase4/frontend/.env.local`):\n   - Updated `NEXT_PUBLIC_AUTH_URL` to `http://localhost:3000`\n   - Updated `BETTER_AUTH_URL` to `http://localhost:3000`\n\n3. **Updated backend CORS configuration** (`phase4/backend/main.py`):\n   - Fixed outdated Vercel URL from Phase 3 to correct Phase 4 URL\n\nThese changes ensure that when running locally, the auth client communicates with the local server instead of the remote Vercel deployment, resolving the CORS issue."
outcome: "CORS authentication issue resolved. Application can now run properly in local development environment without CORS errors."
evaluation: "Success - The authentication flow now works correctly in local development without CORS errors, while maintaining support for production deployments."
---

# Fix CORS Authentication Issue

## Summary
Resolved CORS issue in frontend authentication where the app was incorrectly sending requests to the remote Vercel URL instead of localhost when running locally.

## Changes Made

### 1. Frontend Auth Client Configuration
Updated `phase4/frontend/lib/auth-client.ts` to use environment variable with localhost fallback:
```typescript
baseURL: process.env.NEXT_PUBLIC_AUTH_URL || "http://localhost:3000"
```

### 2. Environment Variables
Updated `phase4/frontend/.env.local` to use localhost for auth URLs:
- `NEXT_PUBLIC_AUTH_URL=http://localhost:3000`
- `BETTER_AUTH_URL=http://localhost:3000`

### 3. Backend CORS Configuration
Updated `phase4/backend/main.py` to use the correct Phase 4 Vercel URL in allowed origins.

## Result
Authentication now works properly in local development without CORS errors, while maintaining production compatibility through environment variables.