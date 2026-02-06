---
id: 001
title: Architect Local K8s and Helm Strategy
stage: plan
date: 2026-02-05
surface: agent
model: claude-sonnet-4-5-20250929
feature: k8s-deployment
branch: 001-k8s-deployment
user: kamlesh_kumar
command: sp.plan "Architecting Phase 4: Local K8s & Helm Strategy"
labels: [architecture, kubernetes, docker, minikube, helm, deployment]
links:
  spec: /home/kamlesh_kumar/projects/Hac2-Phase4-Local-Kubernetes-Deployment/specs/001-k8s-deployment/spec.md
  plan: /home/kamlesh_kumar/projects/Hac2-Phase4-Local-Kubernetes-Deployment/specs/001-k8s-deployment/plan.md
  research: /home/kamlesh_kumar/projects/Hac2-Phase4-Local-Kubernetes-Deployment/specs/001-k8s-deployment/research.md
  data-model: /home/kamlesh_kumar/projects/Hac2-Phase4-Local-Kubernetes-Deployment/specs/001-k8s-deployment/data-model.md
  contracts: /home/kamlesh_kumar/projects/Hac2-Phase4-Local-Kubernetes-Deployment/specs/001-k8s-deployment/contracts/api-contract.md
files:
  - /home/kamlesh_kumar/projects/Hac2-Phase4-Local-Kubernetes-Deployment/specs/001-k8s-deployment/plan.md
  - /home/kamlesh_kumar/projects/Hac2-Phase4-Local-Kubernetes-Deployment/specs/001-k8s-deployment/research.md
  - /home/kamlesh_kumar/projects/Hac2-Phase4-Local-Kubernetes-Deployment/specs/001-k8s-deployment/data-model.md
  - /home/kamlesh_kumar/projects/Hac2-Phase4-Local-Kubernetes-Deployment/specs/001-k8s-deployment/quickstart.md
  - /home/kamlesh_kumar/projects/Hac2-Phase4-Local-Kubernetes-Deployment/specs/001-k8s-deployment/contracts/api-contract.md
tests:
  - none (architectural planning)
---

## Prompt

"Architecting Phase 4: Local K8s & Helm Strategy" ; **OBJECTIVE:**
Generate a comprehensive technical architecture plan (`speckit.plan`) for Phase 4: Local Kubernetes Deployment.

**CONTEXT:**
We have a Next.js Frontend and FastAPI Backend in the `phase4/` directory. We need to define how to containerize them and deploy them to a local Minikube cluster using Helm. The database remains external (Neon Serverless Postgres).

**ARCHITECTURAL DECISIONS TO DOCUMENT:**

1.  **Containerization Strategy (Docker):**
    * **Backend:** Plan for a multi-stage Python build (`python:3.12-slim`) to minimize image size.
    * **Frontend:** Plan for a multi-stage Node.js build (using `output: 'standalone'` in Next.js) for optimization.
    * **AI Ops:** Use Docker AI (Gordon) to generate these Dockerfiles.

2.  **Orchestration Strategy (Kubernetes/Minikube):**
    * **Deployment Objects:** Define Replicas (start with 1 for local), CPU/RAM limits, and Liveness Probes.
    * **Service Objects:**
        * `backend-svc`: **ClusterIP** (Internal only). Frontend talks to this via internal DNS (`http://backend-svc:8000`).
        * `frontend-svc`: **NodePort** or **LoadBalancer** (Exposed to Host). This allows accessing the app from the browser.
    * **Configuration Management:**
        * **Secrets:** Plan to store `DATABASE_URL`, `COHERE_API_KEY`, `BETTER_AUTH_SECRET` as K8s Secrets.
        * **ConfigMaps:** Store non-sensitive configs like `NEXT_PUBLIC_API_URL`.

3.  **Helm Chart Structure:**
    * Create a unified Helm Chart named `todo-app`.
    * Structure: `phase4/k8s/todo-app/` containing `templates/` and `values.yaml`.
    * **AI Ops:** Plan to use `kubectl-ai` to generate the initial manifest files.

4.  **Networking Flow (The Path):**
    * `User Browser` -> `Minikube IP:NodePort` -> `Frontend Pod` -> `Backend Service (DNS)` -> `Backend Pod` -> `External Neon DB (Internet)`.

**OUTPUT:**
Update `speckit.plan` with:
* Component Breakdown (Frontend, Backend, K8s Objects).
* Data Flow Diagram (Text/Mermaid).
* Testing Strategy (How to verify pods are running).

## Response snapshot

Successfully created the comprehensive technical architecture plan for Phase 4: Local Kubernetes Deployment. The plan includes:

1. **Complete implementation plan** (plan.md) with architecture overview, containerization strategy, orchestration strategy, Helm chart structure, and data flow diagram
2. **Research document** (research.md) outlining best practices for Docker multi-stage builds, Kubernetes resource configuration, and Helm chart architecture
3. **Data model** (data-model.md) describing Kubernetes resources, deployment configurations, and relationships
4. **Quickstart guide** (quickstart.md) with step-by-step instructions for setting up and running the application on local Minikube
5. **API contract** (contracts/api-contract.md) defining the service communication protocols between frontend and backend in the Kubernetes environment

The architecture addresses all the user's requirements including multi-stage Docker builds for optimization, proper Kubernetes resource configuration with replicas and resource limits, service objects with ClusterIP for backend and NodePort for frontend, secret management for sensitive configuration, and the complete networking flow.

## Outcome

- ✅ Impact: Complete architecture plan for local Kubernetes deployment with all components documented
- 🧪 Tests: Manual verification of documentation completeness
- 📁 Files: Created plan, research, data-model, quickstart, and contracts documentation
- 🔁 Next prompts: Ready for task breakdown with /sp.tasks
- 🧠 Reflection: Architecture aligns with user requirements and best practices

## Evaluation notes (flywheel)

- Failure modes observed: None - all architectural components properly defined
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin task breakdown for implementation