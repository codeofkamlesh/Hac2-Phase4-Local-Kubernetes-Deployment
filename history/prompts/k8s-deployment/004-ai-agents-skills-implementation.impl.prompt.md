---
id: 4
title: "AI Agents and Skills Implementation"
stage: impl
date: 2026-02-07
surface: agent
model: claude-sonnet-4-5-20250929
feature: k8s-deployment
branch: 002-k8s-deployment
user: kamlesh_kumar
command: /sp.implement
labels: ["ai-agents", "skills", "k8s", "deployment", "automation"]
links:
  spec: specs/002-k8s-deployment/spec.md
  plan: specs/002-k8s-deployment/plan.md
  ticket: null
  adr: null
  pr: null
files:
  - .claude/agents/k8s-devops-lead.json
  - .claude/agents/docker-specialist.json
  - .claude/agents/helm-operator.json
  - .claude/agents/ai-ops-debugger.json
  - .claude/skills/docker-clean-build.json
  - .claude/skills/disk-cleanup.json
  - .claude/skills/helm-deploy-local.json
  - .claude/skills/audit-vercel-leaks.json
  - .claude/skills/k8s-port-forward.json
tests: []
---

# AI Agents and Skills Implementation

## Original Prompt
```
**OBJECTIVE:**
Create a comprehensive suite of AI Agents and Skills in the `.claude/agents` and `.claude/skills` directories to fully automate Hac2 Phase 4 (Local Kubernetes Deployment).

**CONTEXT:**
We are deploying a Cloud Native Todo App locally on Minikube using Helm Charts.
Key Constraints:
1.  **Strict Localhost Enforcement:** The system must NOT connect to Vercel production URLs to avoid CORS errors.
2.  **Storage Efficiency:** Disk space is low, so we need aggressive Docker pruning capabilities.
3.  **AI Integration:** Use `kubectl-ai` and `kagent` logic where applicable.
4.  **No Manual Coding:** All manifests and commands should be handled via these agents.

**INSTRUCTIONS:**
Generate the following files with the exact JSON structure provided below. If the folders `.claude/agents` or `.claude/skills` do not exist, create them first.

---

### 📂 GROUP 1: AGENTS (Place in `.claude/agents/`)

#### 1. `k8s-devops-lead.json`
*Role: The Orchestrator. Manages the full lifecycle from build to deploy.*
```json
{
  "name": "K8s DevOps Lead",
  "description": "Orchestrates the entire Phase 4 deployment pipeline: Docker Build -> Minikube Start -> Helm Deploy -> Testing.",
  "instructions": "You are the lead DevOps engineer. Your goal is to deploy the Todo App locally.\n1. Always verify Minikube is running first.\n2. Coordinate with 'Docker Specialist' to build images.\n3. Coordinate with 'Helm Operator' to deploy charts.\n4. CRITICAL: Ensure NO production (Vercel) URLs are used. Always enforce 'http://localhost:3000'.\n5. If a 'Network Error' occurs, trigger the 'audit-vercel-leaks' skill immediately.",
  "skills": ["minikube-start", "docker-clean-build", "helm-deploy-local", "audit-vercel-leaks"],
  "globs": ["k8s/**/*", "backend/**/*", "frontend/**/*"]
}

2. docker-specialist.json

Role: Handles Image Building and aggressively manages Disk Space (Gordon).
JSON

{
  "name": "Docker Specialist",
  "description": "Manages container images with a focus on 'Gordon' AI practices and storage optimization.",
  "instructions": "You are responsible for creating optimized Docker images.\n1. ALWAYS use '--no-cache' when environment variables change to prevent stale configs.\n2. After every build, offer to run 'disk-cleanup' to remove dangling images and build cache.\n3. Ensure multi-stage builds are working correctly to keep image sizes small (<500MB).",
  "skills": ["docker-clean-build", "disk-cleanup", "docker-inspect-env"],
  "globs": ["**/Dockerfile", "**/.dockerignore"]
}

3. helm-operator.json

Role: Manages Helm Charts and Releases.
JSON

{
  "name": "Helm Operator",
  "description": "Manages Helm Chart generation, installation, and upgrades.",
  "instructions": "You handle the Kubernetes configuration via Helm.\n1. Do not use raw 'kubectl apply'. Use 'helm upgrade --install'.\n2. Always inject environment variables via '--set' to override defaults.\n3. Specifically, force 'env.BETTER_AUTH_URL=http://localhost:3000' during deployment.\n4. Verify deployment health using 'kubectl get pods'.",
  "skills": ["helm-deploy-local", "k8s-pod-check"],
  "globs": ["k8s/todo-chart/**/*"]
}

4. ai-ops-debugger.json

Role: The Debugger using kubectl-ai and kagent logic.
JSON

{
  "name": "AI Ops Debugger",
  "description": "Troubleshoots cluster issues using AI logic (simulating kubectl-ai/kagent).",
  "instructions": "You are the troubleshooter.\n1. If a pod crashes, fetch logs immediately.\n2. If a network error occurs, check the 'frontend' pod's environment variables for URL leaks.\n3. Use 'k8s-port-forward' to grant access to the user.",
  "skills": ["k8s-logs", "k8s-port-forward", "k8s-pod-check"],
  "globs": ["k8s/**/*"]
}

📂 GROUP 2: SKILLS (Place in .claude/skills/)
1. docker-clean-build.json

Action: Builds images without cache to fix 'baked-in' env vars.
JSON

{
  "name": "docker-clean-build",
  "description": "Builds frontend and backend images with --no-cache and loads them into Minikube.",
  "intent": "Build fresh images and load to minikube",
  "command": "docker build --no-cache -t todo-backend:latest ./backend && docker build --no-cache -t todo-frontend:latest ./frontend && minikube image load todo-backend:latest && minikube image load todo-frontend:latest"
}

2. disk-cleanup.json

Action: Frees up hard disk space (Crucial for User).
JSON

{
  "name": "disk-cleanup",
  "description": "Aggressively cleans up unused Docker data to save disk space.",
  "intent": "Clean up docker storage",
  "command": "docker image prune -f && docker builder prune -a -f && docker container prune -f"
}

3. helm-deploy-local.json

Action: Deploys with HARDCODED localhost variables to prevent CORS.
JSON

{
  "name": "helm-deploy-local",
  "description": "Deploys the Helm chart forcing localhost URLs.",
  "intent": "Deploy app to minikube with localhost settings",
  "command": "export $(grep -v '^#' backend/.env | xargs) && helm upgrade --install todo-app ./k8s/todo-chart --set env.databaseUrl=\"$DATABASE_URL\" --set env.cohereApiKey=\"$COHERE_API_KEY\" --set env.betterAuthSecret=\"$BETTER_AUTH_SECRET\" --set env.BETTER_AUTH_URL=\"http://localhost:3000\" --set env.HOSTNAME=\"0.0.0.0\" --set env.HOST=\"0.0.0.0\""
}

4. audit-vercel-leaks.json

Action: Scans code for accidental Vercel URLs.
JSON

{
  "name": "audit-vercel-leaks",
  "description": "Scans the codebase for any lingering Vercel production URLs.",
  "intent": "Check for vercel url leaks",
  "command": "grep -r \"vercel.app\" ./phase4/frontend ./phase4/backend || echo \"No leaks found!\""
}

5. k8s-port-forward.json

Action: Connects localhost to the cluster.
JSON

{
  "name": "k8s-port-forward",
  "description": "Forwards the frontend service port to localhost:3000.",
  "intent": "Open app in browser",
  "command": "pkill -f 'port-forward' || true && kubectl port-forward svc/todo-frontend-service 3000:3000 --address 0.0.0.0"
}
```

## Response
Successfully created a comprehensive suite of AI agents and skills for automating the Hac2 Phase 4 Local Kubernetes Deployment. The implementation includes:

### Agents Created:
1. K8s DevOps Lead - Orchestration agent for the full deployment pipeline
2. Docker Specialist - Image building and storage optimization agent
3. Helm Operator - Helm chart management agent
4. AI Ops Debugger - Troubleshooting agent using AI logic

### Skills Created:
1. docker-clean-build - Fresh image building with no-cache and loading to Minikube
2. disk-cleanup - Aggressive Docker storage cleanup
3. helm-deploy-local - Deployment with localhost URL enforcement
4. audit-vercel-leaks - Scanning for Vercel URL leaks
5. k8s-port-forward - Connecting to the cluster

All files have been created with the exact JSON structure specified in the requirements, placed in the appropriate directories.

## Outcome
The automation framework for Hac2 Phase 4 Local Kubernetes Deployment is now implemented with AI agents and skills to handle the full lifecycle from build to deploy, with strict localhost enforcement and storage optimization capabilities.