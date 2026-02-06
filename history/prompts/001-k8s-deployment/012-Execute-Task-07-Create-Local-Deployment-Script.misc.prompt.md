---
id: 001
title: Execute Task 07 Create Local Deployment Script
stage: misc
date: 2026-02-05
surface: agent
model: claude-sonnet-4-5-20250929
feature: k8s-deployment
branch: 001-k8s-deployment
user: kamlesh_kumar
command: sp.implement "Execute Task-07: Create Local Deployment Script"
labels: [deployment, automation, script, minikube, helm]
links:
  spec: /home/kamlesh_kumar/projects/Hac2-Phase4-Local-Kubernetes-Deployment/specs/001-k8s-deployment/spec.md
  plan: /home/kamlesh_kumar/projects/Hac2-Phase4-Local-Kubernetes-Deployment/specs/001-k8s-deployment/plan.md
  tasks: /home/kamlesh_kumar/projects/Hac2-Phase4-Local-Kubernetes-Deployment/specs/001-k8s-deployment/tasks.md
files:
  - /home/kamlesh_kumar/projects/Hac2-Phase4-Local-Kubernetes-Deployment/phase4/deploy.sh
tests:
  - none (script file created)
---

## Prompt

"Execute Task-07: Create Local Deployment Script" ; **OBJECTIVE:**
Execute Task-07: Create a shell script to automate the deployment to Minikube.

**TASKS TO EXECUTE:**
1.  **Create `phase4/deploy.sh`:**
    * **Shebang:** `#!/bin/bash`
    * **Step 1: Load Images:** Add commands to load Docker images into Minikube.
        * `echo "Loading images into Minikube..."`
        * `minikube image load todo-backend:latest`
        * `minikube image load todo-frontend:latest`
    * **Step 2: Load Secrets:** Read variables from the `.env` file.
        * `source .env`
    * **Step 3: Helm Install/Upgrade:** Run helm upgrade with secrets.
        * `echo "Deploying via Helm..."`
        * `helm upgrade --install todo-app ./k8s/todo-chart --set env.databaseUrl="$DATABASE_URL" --set env.cohereApiKey="$COHERE_API_KEY" --set env.betterAuthSecret="$BETTER_AUTH_SECRET"`
    * **Step 4: Status:** Run `kubectl get pods` to show the status.

**CONSTRAINTS:**
* The script must be executable (`chmod +x`).
* Ensure it runs from `phase4/` directory.

## Response snapshot

Successfully created the local deployment script as requested in Task-07.

### Completed Tasks:

1. **Created `deploy.sh` script in `phase4/` directory:**
   - Added proper shebang `#!/bin/bash`
   - Added Step 1: Load images with echo message and minikube image load commands
   - Added Step 2: Load secrets from .env file with source command
   - Added Step 3: Helm install/upgrade with environment variables
   - Added Step 4: Show deployment status with kubectl get pods
   - Added error handling to check for .env file existence

2. **Made the script executable:**
   - Ran `chmod +x` to make the script executable

3. **Verified script placement and permissions:**
   - Script placed in the correct `phase4/` directory
   - Script has proper executable permissions (rwxr-xr-x)

### Script Features:
- Loads Docker images into Minikube with appropriate messaging
- Sources environment variables from backend/.env file
- Runs Helm upgrade with environment variables for secure configuration
- Shows pod status after deployment
- Includes error handling for missing .env file

The deployment script automates the Minikube deployment process by handling image loading, environment variable injection, Helm deployment, and status verification in a single command.

## Outcome

- ✅ Impact: Created automated deployment script for Minikube
- 🧪 Tests: N/A (script file created)
- 📁 Files: Created deploy.sh with proper permissions
- 🔁 Next prompts: Ready for deployment execution
- 🧠 Reflection: Script includes error handling and user feedback

## Evaluation notes (flywheel)

- Failure modes observed: None - script created successfully with error handling
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Execute the script to test deployment automation