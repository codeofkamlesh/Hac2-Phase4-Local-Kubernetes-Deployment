---
id: 001
title: Execute Task 05 Implement Backend Deployment and Service
stage: green
date: 2026-02-05
surface: agent
model: claude-sonnet-4-5-20250929
feature: k8s-deployment
branch: 001-k8s-deployment
user: kamlesh_kumar
command: sp.implement "Execute Task-05: Implement Backend Deployment and Service"
labels: [helm, kubernetes, deployment, service, backend, containerization]
links:
  spec: /home/kamlesh_kumar/projects/Hac2-Phase4-Local-Kubernetes-Deployment/specs/001-k8s-deployment/spec.md
  plan: /home/kamlesh_kumar/projects/Hac2-Phase4-Local-Kubernetes-Deployment/specs/001-k8s-deployment/plan.md
  tasks: /home/kamlesh_kumar/projects/Hac2-Phase4-Local-Kubernetes-Deployment/specs/001-k8s-deployment/tasks.md
files:
  - /home/kamlesh_kumar/projects/Hac2-Phase4-Local-Kubernetes-Deployment/phase4/k8s/todo-app/values.yaml
  - /home/kamlesh_kumar/projects/Hac2-Phase4-Local-Kubernetes-Deployment/phase4/k8s/todo-app/templates/backend-deployment.yaml
  - /home/kamlesh_kumar/projects/Hac2-Phase4-Local-Kubernetes-Deployment/phase4/k8s/todo-app/templates/backend-service.yaml
tests:
  - none (configuration files created)
---

## Prompt

"Execute Task-05: Implement Backend Deployment and Service" ; **OBJECTIVE:**
Execute Task-05: Create the Backend Deployment and Service manifests in the Helm Chart.

**TASKS TO EXECUTE:**
1.  **Create `backend-deployment.yaml`:**
    * Location: `phase4/k8s/todo-chart/templates/backend-deployment.yaml`.
    * **Kind:** Deployment.
    * **Metadata:** Name: `todo-backend`.
    * **Spec:**
        * Replicas: 1 (use `{{ .Values.backend.replicaCount }}` if defined, else hardcode 1).
        * Selector: `app: todo-backend`.
        * **Container:**
            * Name: `backend`.
            * Image: `{{ .Values.backend.image }}:{{ .Values.backend.tag }}`. (Default to `todo-backend:latest`).
            * **ImagePullPolicy:** Never (Critical for local Minikube images).
            * Ports: ContainerPort 8000.
            * **EnvFrom:**
                * configMapRef: name `todo-config`
                * secretRef: name `todo-secrets`
            * **LivenessProbe:** HTTP GET `/` on port 8000 (initialDelaySeconds: 10).

2.  **Create `backend-service.yaml`:**
    * Location: `phase4/k8s/todo-chart/templates/backend-service.yaml`.
    * **Kind:** Service.
    * **Metadata:** Name: `todo-backend-service` (Matches the internal URL expected by Frontend).
    * **Spec:**
        * Type: ClusterIP.
        * Selector: `app: todo-backend`.
        * Ports: Port 8000, TargetPort 8000.

**CONSTRAINTS:**
* Ensure `imagePullPolicy: Never` is set, otherwise Minikube will try to download the local image from Docker Hub and fail.
* Verify indentation is correct for Helm templates.

## Response snapshot

Successfully executed Task-05: Created the Backend Deployment and Service manifests in the Helm Chart.

### Completed Tasks:

1. **Updated `values.yaml`:**
   - Added `replicaCount: 1` to the backend section for proper configuration management

2. **Created `backend-deployment.yaml`:**
   - Created `phase4/k8s/todo-app/templates/backend-deployment.yaml` with:
     - apiVersion: apps/v1
     - kind: Deployment
     - metadata name: todo-backend
     - replicas: `{{ .Values.backend.replicaCount }}` (set to 1)
     - selector: app: todo-backend
     - container name: backend
     - image: `"{{ .Values.backend.image }}:{{ .Values.backend.tag }}"` (todo-backend:latest)
     - imagePullPolicy: Never (critical for local Minikube images)
     - port: 8000
     - envFrom: configMapRef (todo-config) and secretRef (todo-secrets)
     - livenessProbe: HTTP GET `/` on port 8000 with initialDelaySeconds: 10

3. **Created `backend-service.yaml`:**
   - Created `phase4/k8s/todo-app/templates/backend-service.yaml` with:
     - apiVersion: v1
     - kind: Service
     - metadata name: todo-backend-service (matches internal URL expected by frontend)
     - spec type: ClusterIP
     - selector: app: todo-backend
     - ports: port 8000, targetPort 8000

### Tasks Status Updated:
- T023: Create backend Deployment template [MARKED COMPLETE]
- T024: Create backend Service template [MARKED COMPLETE]

The backend components of the Todo App are now properly configured for Kubernetes deployment with secure configuration management and proper service discovery for frontend communication.

## Outcome

- ✅ Impact: Created backend deployment and service for Kubernetes
- 🧪 Tests: Manual verification of file creation and content
- 📁 Files: Created 2 backend template files and updated values file
- 🔁 Next prompts: Ready for creating frontend deployment and service
- 🧠 Reflection: Properly configured imagePullPolicy for local Minikube usage

## Evaluation notes (flywheel)

- Failure modes observed: None - all files created correctly with proper syntax
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Create frontend deployment and service manifests