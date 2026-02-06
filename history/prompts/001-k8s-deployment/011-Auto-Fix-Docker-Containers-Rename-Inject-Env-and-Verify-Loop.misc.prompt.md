---
id: 001
title: Auto Fix Docker Containers Rename Inject Env and Verify Loop
stage: misc
date: 2026-02-05
surface: agent
model: claude-sonnet-4-5-20250929
feature: k8s-deployment
branch: 001-k8s-deployment
user: kamlesh_kumar
command: sp.implement "Auto-Fix Docker Containers: Rename, Inject Env, and Verify Loop"
labels: [docker, environment, containerization, troubleshooting]
links:
  spec: /home/kamlesh_kumar/projects/Hac2-Phase4-Local-Kubernetes-Deployment/specs/001-k8s-deployment/spec.md
  plan: /home/kamlesh_kumar/projects/Hac2-Phase4-Local-Kubernetes-Deployment/specs/001-k8s-deployment/plan.md
  tasks: /home/kamlesh_kumar/projects/Hac2-Phase4-Local-Kubernetes-Deployment/specs/001-k8s-deployment/tasks.md
files:
  - /home/kamlesh_kumar/projects/Hac2-Phase4-Local-Kubernetes-Deployment/phase4/backend/.env
  - /home/kamlesh_kumar/projects/Hac2-Phase4-Local-Kubernetes-Deployment/specs/001-k8s-deployment/quickstart.md
tests:
  - none (documentation and procedure)
---

## Prompt

"Auto-Fix Docker Containers: Rename, Inject Env, and Verify Loop" ; **OBJECTIVE:**
Fix the repeated "DATABASE_URL not set" error in the Backend, rename both containers to standard names, and ensure BOTH are running simultaneously.

**CONTEXT:**
The user is facing a crash in the backend container due to missing environment variables. Current container names are random (e.g., `vigorous_pare`).

**INSTRUCTIONS (Execute in Order):**

1.  **CLEANUP (Force Remove Old):**
    * Stop and remove ALL running or exited containers related to this project to clear the slate.
    * Command: `docker rm -f container-todo-backend container-todo-frontend quirky_brahmagupta tender_nightingale vigorous_pare` (ignore errors if they don't exist).

2.  **LOCATE .ENV (Crucial Step):**
    * Find the absolute path of the `.env` file. Do not guess.
    * Command: `find $(pwd)/../ -name ".env" | head -n 1` (Adjust search depth if needed).
    * Store this path in a variable, e.g., `ENV_PATH`.

3.  **RUN BACKEND (With Fix):**
    * Run the backend using the *verified* `.env` path and the specific name.
    * Command: `docker run --rm -d -p 8000:8000 --env-file "$ENV_PATH" --name container-todo-backend todo-backend`

4.  **RUN FRONTEND:**
    * Command: `docker run --rm -d -p 3000:3000 --name container-todo-frontend todo-frontend`

5.  **VALIDATION & SELF-REPAIR LOOP:**
    * Wait 5 seconds (`sleep 5`).
    * Check status: `docker ps`.
    * **IF BACKEND IS MISSING:**
        * View logs: `docker logs container-todo-backend` (or the ID if it exited).
        * If it failed due to env vars, TRY AGAIN by hardcoding the env vars from the file directly into the command (using multiple `-e KEY=VALUE` flags) instead of `--env-file`.
    * **SUCCESS CRITERIA:** Both `container-todo-backend` and `container-todo-frontend` must appear in `docker ps` with Status "Up".

**OUTPUT:**
Show the final `docker ps` table confirming both are running.

## Response snapshot

Docker container management task cannot be executed in this environment. However, I can provide the complete documented procedure for fixing the Docker containers:

### Issue Identified:
The backend container fails with "DATABASE_URL environment variable is not set" error when running with Docker directly because the required environment variables are not being passed to the container.

### Solution Procedure:

#### 1. Environment File Location:
- Located: `/home/kamlesh_kumar/projects/Hac2-Phase4-Local-Kubernetes-Deployment/phase4/backend/.env`
- Contains essential variables: DATABASE_URL, BETTER_AUTH_SECRET, COHERE_API_KEY, etc.

#### 2. Cleanup Commands:
```bash
# Stop and remove old containers (will return error if containers don't exist, which is normal)
docker rm -f container-todo-backend container-todo-frontend quirky_brahmagupta tender_nightingale vigorous_pare || true
```

#### 3. Start Backend Container:
```bash
# Navigate to the phase4 directory first
cd /home/kamlesh_kumar/projects/Hac2-Phase4-Local-Kubernetes-Deployment/phase4

# Set the environment file path
ENV_PATH="../phase4/backend/.env"

# Run the backend container with environment variables and standardized name
docker run --rm -d -p 8000:8000 --env-file "$ENV_PATH" --name container-todo-backend todo-backend
```

#### 4. Start Frontend Container:
```bash
docker run --rm -d -p 3000:3000 --name container-todo-frontend todo-frontend
```

#### 5. Validation Steps:
```bash
# Wait for containers to start
sleep 5

# Check running containers
docker ps

# If backend container is not running, check the logs:
docker logs container-todo-backend

# Alternative: If the --env-file approach fails, use explicit environment variables:
docker run --rm -d -p 8000:8000 \
  -e DATABASE_URL="postgresql://neondb_owner:npg_o4vtlc5qVnZI@ep-quiet-grass-a7i6iu10-pooler.ap-southeast-2.aws.neon.tech/neondb?sslmode=require" \
  -e BETTER_AUTH_SECRET="JXHCNmiHGxZ1DSN3jUW0RMt9YbdEC7He" \
  -e CO_API_KEY="2ySJyl0YL0n42dQUySE6D6NSWW8SBOqFKOwlGUhs" \
  -e COHERE_API_KEY="2ySJyl0YL0n42dQUySE6D6NSWW8SBOqFKOwlGUhs" \
  --name container-todo-backend todo-backend
```

#### 6. Expected Output:
After running `docker ps`, you should see both containers:
```
CONTAINER ID   IMAGE             COMMAND                  CREATED        STATUS        PORTS                            NAMES
xxx            todo-backend      "uvicorn main:app ..."   X seconds ago  Up X secs     0.0.0.0:8000->8000/tcp          container-todo-backend
yyy            todo-frontend     "docker-entrypoint.s..." X seconds ago  Up X secs     0.0.0.0:3000->3000/tcp          container-todo-frontend
```

#### 7. Verification:
- Access the backend at http://localhost:8000
- Access the frontend at http://localhost:3000
- Both containers should show "Up" status in `docker ps`

### Troubleshooting:
If the backend container still fails:
1. Check the logs with `docker logs container-todo-backend`
2. Ensure the `todo-backend` image exists: `docker images | grep todo-backend`
3. Verify the .env file has the correct values
4. Make sure you're running the command from the correct directory

## Outcome

- ✅ Impact: Documented complete procedure to fix Docker container environment issue
- 🧪 Tests: Manual verification when procedure is executed
- 📁 Files: Referenced .env file location for environment variables
- 🔁 Next prompts: Ready to execute the Docker commands on a system with Docker access
- 🧠 Reflection: Environment variables are critical for backend startup in containerized deployments

## Evaluation notes (flywheel)

- Failure modes observed: Missing environment variables causing backend container startup failure
- Graders run and results (PASS/FAIL): N/A (procedure documented, cannot execute in this environment)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Execute the documented procedure on a system with Docker access