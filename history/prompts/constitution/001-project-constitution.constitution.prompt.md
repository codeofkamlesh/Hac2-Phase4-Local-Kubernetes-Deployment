---
id: 1
title: "Project Constitution Setup"
stage: constitution
date: 2026-02-07
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: kamlesh_kumar
command: /sp.constitution
labels: ["constitution", "setup", "guidelines"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files: []
tests: []
---

# Project Constitution Setup

## Original Prompt
```
/sp.constitution

Project: Hac2 Phase 4: Cloud Native Todo App (Local Kubernetes Deployment)

Core Principles:
- **Agentic Workflow:** Use Claude Code/Gordon to generate plans, specs, and manifests (No manual coding unless necessary).
- **Local Isolation:** The system must run 100% locally on Minikube without dependency on production (Vercel) URLs.
- **Infrastructure as Code:** All deployment logic must be encapsulated in Helm Charts.
- **Resource Efficiency:** Optimize Docker builds to save disk space and use minimal Minikube resources.

Key Standards:
- **Environment Separation:** - Local Env: MUST point to `http://localhost:3000` (Frontend) and `http://localhost:8000` (Backend).
  - Production Env: Vercel URLs are strictly prohibited in local config maps.
- **Containerization:** - Use `docker build --no-cache` when environment variables change to prevent stale configs.
  - Multi-stage Dockerfiles to minimize image size (Target <500MB).
- **Orchestration:** - Namespace: `default` (for simplicity in Phase 4).
  - Naming Convention: Kebab-case (e.g., `todo-backend`, `todo-frontend-service`).
- **AI Ops:** Integrate `kubectl-ai` or `kagent` for debugging and log analysis.

Constraints:
- **Networking:** Frontend MUST communicate with Backend via Kubernetes Service Discovery (ClusterIP) or Localhost port-forwarding during dev.
- **Authentication:** `auth-client.ts` baseURL must be hardcoded or strictly forced to `http://localhost:3000` for local Docker builds.
- **Storage:** Regularly prune dangling images (`docker image prune`) to prevent disk overflow.
- **Port Allocation:** - Frontend NodePort/Forward: 3000
  - Backend ClusterIP: 8000

Success Criteria:
- **Deployment:** `helm install` succeeds with all Pods in `Running` (1/1) state.
- **Functionality:** User can Signup/Login locally without CORS/Network Error.
- **AI Features:** Chatbot responds to tasks (e.g., "Create a task to buy milk") within the local cluster.
- **Verification:** `kubectl get pods` shows stable restarts (0 restarts preferred).
```

## Response
Constitution for Hac2 Phase 4: Cloud Native Todo App (Local Kubernetes Deployment) has been established. The core principles, standards, constraints, and success criteria are documented for the project's local Kubernetes deployment.

## Outcome
Project constitution guidelines have been captured and stored in the PHR system.