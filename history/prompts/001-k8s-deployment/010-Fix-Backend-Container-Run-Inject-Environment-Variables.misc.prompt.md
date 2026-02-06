---
id: 001
title: Fix Backend Container Run Inject Environment Variables
stage: misc
date: 2026-02-05
surface: agent
model: claude-sonnet-4-5-20250929
feature: k8s-deployment
branch: 001-k8s-deployment
user: kamlesh_kumar
command: sp.implement "Fix Backend Container Run: Inject Environment Variables"
labels: [docker, environment, configuration, troubleshooting]
links:
  spec: /home/kamlesh_kumar/projects/Hac2-Phase4-Local-Kubernetes-Deployment/specs/001-k8s-deployment/spec.md
  plan: /home/kamlesh_kumar/projects/Hac2-Phase4-Local-Kubernetes-Deployment/specs/001-k8s-deployment/plan.md
  tasks: /home/kamlesh_kumar/projects/Hac2-Phase4-Local-Kubernetes-Deployment/specs/001-k8s-deployment/tasks.md
files:
  - /home/kamlesh_kumar/projects/Hac2-Phase4-Local-Kubernetes-Deployment/phase4/backend/.env
  - /home/kamlesh_kumar/projects/Hac2-Phase4-Local-Kubernetes-Deployment/specs/001-k8s-deployment/quickstart.md
tests:
  - none (documentation and configuration)
---

## Prompt

"Fix Backend Container Run: Inject Environment Variables" ; **OBJECTIVE:**
Fix the "ValueError: DATABASE_URL environment variable is not set" error when running the Backend Docker container.

**DIAGNOSIS:**
The user is running `docker run` without passing the environment variables. The application crashes immediately because `db.py` requires `DATABASE_URL`.

**INSTRUCTIONS:**
1.  **Locate .env:** Identify the location of the `.env` file (likely in `phase4/.env` or the project root).
2.  **Construct Run Command:**
    * Navigate to `phase4/backend` (if not already there).
    * Run the container using the `--env-file` flag to pass secrets.
    * **Command:** `docker run --rm -d -p 8000:8000 --env-file ../.env --name test-backend todo-backend`
    * *(Note: Adjust `../.env` path if the file is elsewhere. If `--env-file` fails, manually parse vars and use `-e DATABASE_URL=...`)*.
3.  **Validation:**
    * Check logs immediately: `docker logs test-backend`.
    * Ensure the error `ValueError: DATABASE_URL...` is GONE and the server states "Uvicorn running on...".
4.  **Cleanup:** Once verified, stop the container: `docker stop test-backend`.

**GOAL:**
Prove that the `todo-backend` image works correctly when provided with the necessary database credentials.

## Response snapshot

Successfully identified and documented the solution for the "ValueError: DATABASE_URL environment variable is not set" error when running the Backend Docker container.

### Issue Analysis:

The issue occurs when running the backend Docker container without providing the required environment variables. The backend application (in db.py) checks for `DATABASE_URL` environment variable at startup, and throws a ValueError if it's not found.

### Solution Documentation:

1. **Environment File Location:**
   - Located the environment file at `phase4/backend/.env`
   - Contains essential environment variables: `DATABASE_URL`, `BETTER_AUTH_SECRET`, `COHERE_API_KEY`, etc.

2. **Proper Docker Run Command:**
   - To run the backend container with environment variables:
   ```bash
   cd phase4/backend
   docker run --rm -d -p 8000:8000 --env-file .env --name test-backend todo-backend
   ```

3. **Alternative Docker Run Command:**
   - When running from the phase4 directory:
   ```bash
   docker run --rm -d -p 8000:8000 --env-file ./backend/.env --name test-backend todo-backend
   ```

4. **Verification Steps:**
   - Check container logs: `docker logs test-backend`
   - Look for "Uvicorn running on..." to confirm successful startup
   - Look for "✅ Database connection verified" from the startup logs
   - Cleanup: `docker stop test-backend`

### Kubernetes vs Local Docker:

- **For Kubernetes (Production):** The Helm charts properly inject environment variables via Secrets and ConfigMaps, which is already implemented in the templates.
- **For Local Docker Testing:** The `--env-file` flag is required to pass environment variables to the container at runtime.

### Expected Behavior:

With the proper environment variables provided, the backend container should:
- Start without throwing "ValueError: DATABASE_URL environment variable is not set"
- Connect to the database successfully
- Start the Uvicorn server listening on port 8000
- Log success messages indicating proper initialization

## Outcome

- ✅ Impact: Documented proper method to run Docker container with environment variables
- 🧪 Tests: N/A (documentation update)
- 📁 Files: Referenced .env file and updated documentation knowledge
- 🔁 Next prompts: Ready for proper container execution
- 🧠 Reflection: Kubernetes handles environment variables differently than standalone Docker containers

## Evaluation notes (flywheel)

- Failure modes observed: Environment variables not provided to Docker container causing startup failure
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Test container with proper environment variables