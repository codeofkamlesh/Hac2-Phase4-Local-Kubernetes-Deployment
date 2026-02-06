# Quickstart Guide: Phase 4: Local Kubernetes Deployment

**Feature**: 001-k8s-deployment
**Date**: 2026-02-05

## Overview

This guide provides step-by-step instructions for setting up and running the Todo application on a local Kubernetes cluster using Minikube and Helm.

## Prerequisites

- Docker Desktop or Docker Engine installed and running
- Minikube (latest version)
- Helm 3.x
- kubectl
- kubectl-ai (optional, for AI operations)
- Node.js and npm (for local development verification)

## Setup Instructions

### 1. Start Minikube Cluster

```bash
# Start Minikube with sufficient resources
minikube start --cpus=4 --memory=8192 --disk-size=20g

# Enable required addons
minikube addons enable ingress
minikube addons enable metrics-server
```

### 2. Prepare Environment Variables

Create a local `.env` file with the required configuration:

```bash
# Example .env file
DATABASE_URL="your_neon_database_url"
COHERE_API_KEY="your_cohere_api_key"
BETTER_AUTH_SECRET="your_auth_secret"
NEXT_PUBLIC_API_URL="http://$(minikube ip):NODEPORT"
```

### 3. Build Docker Images

Navigate to the phase4 directory:

```bash
cd phase4

# Build backend image
cd backend
docker build -t todo-backend:latest .

# Build frontend image
cd ../frontend
docker build -t todo-frontend:latest .

# Verify images were created
docker images | grep todo
```

### 4. Load Images into Minikube

```bash
# Load images into Minikube's container registry
minikube image load todo-backend:latest
minikube image load todo-frontend:latest
```

### 5. Create Kubernetes Secrets

```bash
# Create namespace (optional but recommended)
kubectl create namespace todo-app

# Create secrets
kubectl create secret generic app-secrets \
  --from-literal=DATABASE_URL="your_neon_database_url" \
  --from-literal=COHERE_API_KEY="your_cohere_api_key" \
  --from-literal=BETTER_AUTH_SECRET="your_auth_secret"
```

### 6. Install Helm Chart

```bash
# Navigate to the Helm chart directory
cd ../k8s/todo-app

# Install the chart
helm install todo-app . --namespace todo-app --create-namespace

# Or upgrade if already installed
helm upgrade todo-app . --namespace todo-app --install
```

### 7. Verify Installation

```bash
# Check pods status
kubectl get pods --namespace todo-app

# Check services
kubectl get svc --namespace todo-app

# Check deployments
kubectl get deployments --namespace todo-app

# View logs for backend
kubectl logs -l app=backend --namespace todo-app

# View logs for frontend
kubectl logs -l app=frontend --namespace todo-app
```

## Access the Application

### Get the NodePort

```bash
# Get the NodePort for the frontend service
kubectl get svc frontend-service --namespace todo-app -o jsonpath="{.spec.ports[0].nodePort}"

# Access the application
echo "Visit: http://$(minikube ip):NODEPORT"
```

### Or Use Minikube Service Command

```bash
# Open the service in browser (may need to run in background)
minikube service frontend-service --namespace todo-app --url
```

## Troubleshooting

### Common Issues

1. **Pod stuck in Pending state**:
   ```bash
   kubectl describe pods --namespace todo-app
   ```

2. **Service not accessible**:
   ```bash
   kubectl get nodes -o wide
   minikube ip
   ```

3. **ImagePullBackOff**:
   ```bash
   # Ensure images are loaded into minikube
   minikube image load todo-backend:latest
   minikube image load todo-frontend:latest
   ```

4. **Connection to database failing**:
   ```bash
   # Check environment variables in pods
   kubectl exec -it <pod-name> --namespace todo-app -- env
   ```

### Useful Commands

```bash
# View all resources in namespace
kubectl get all --namespace todo-app

# Port forward for debugging
kubectl port-forward -n todo-app svc/backend-service 8000:8000

# Get detailed status of deployments
kubectl rollout status deployment/backend-deployment --namespace todo-app

# Scale deployments
kubectl scale deployment backend-deployment --replicas=2 --namespace todo-app
```

## AI-Enhanced Operations

If kubectl-ai is installed, you can use natural language commands:

```bash
# Examples of AI operations
kubectl-ai "show me all pods in todo-app namespace"
kubectl-ai "restart the backend deployment"
kubectl-ai "scale frontend to 2 replicas"
kubectl-ai "get logs from failed pods"
```

## Cleanup

```bash
# Uninstall the Helm release
helm uninstall todo-app --namespace todo-app

# Delete the namespace
kubectl delete namespace todo-app

# Stop Minikube
minikube stop

# Optionally delete Minikube cluster completely
minikube delete
```

## Development Workflow

### Iterate on Docker Images

1. Make changes to backend/frontend code
2. Rebuild Docker images with new tags
3. Load new images to Minikube
4. Update Helm values with new image tags
5. Upgrade Helm release

```bash
# Example iterative development
docker build -t todo-backend:v2 .
minikube image load todo-backend:v2
helm upgrade todo-app . --set backend.image.tag=v2 --namespace todo-app
```

## Monitoring Health

The application should expose health endpoints:

- Backend health: `GET /health` on backend service
- Frontend health: `GET /api/health` on frontend service (proxies to backend)

You can check these through port forwarding:

```bash
kubectl port-forward -n todo-app svc/backend-service 8000:8000 &
curl http://localhost:8000/health
```