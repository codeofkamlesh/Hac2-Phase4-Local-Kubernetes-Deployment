# Quickstart Guide: Phase 4: Local Kubernetes Deployment & AI Ops Integration

## Prerequisites

Before starting the deployment, ensure you have the following tools installed:

- **Docker Desktop** (with Kubernetes disabled if using Minikube)
- **Minikube** (v1.35+)
- **Helm** (v3+)
- **kubectl**
- **kubectl-ai** (optional, for AI Ops features)
- **Gordon** (optional, for Docker optimization)

## Deployment Steps

### 1. Start Minikube

```bash
# Start Minikube with sufficient resources for the application
minikube start --cpus=4 --memory=8192 --driver=docker

# Verify Minikube is running
minikube status
```

### 2. Build Docker Images

```bash
# Navigate to the project root
cd /path/to/Hac2-Phase4-Local-Kubernetes-Deployment

# Build optimized frontend image
docker build -f ./docker/frontend.Dockerfile -t todo-frontend:latest --no-cache .

# Build optimized backend image
docker build -f ./docker/backend.Dockerfile -t todo-backend:latest --no-cache .
```

### 3. Load Images into Minikube

```bash
# Load images into Minikube's container registry
minikube image load todo-frontend:latest
minikube image load todo-backend:latest

# Verify images are loaded
minikube ssh docker images | grep todo
```

### 4. Deploy with Helm

```bash
# Navigate to helm directory
cd ./phase4/helm

# Install the application using Helm
helm install todo-app todo-app/ --values todo-app/values.yaml

# Verify all pods are running
kubectl get pods
```

### 5. Access the Application

```bash
# The frontend should be accessible at http://localhost:3000
# Port forward to access the frontend if needed
kubectl port-forward svc/todo-frontend-service 3000:3000

# The backend is available internally at http://todo-backend-service:8000
# Port forward to access the backend if needed
kubectl port-forward svc/todo-backend-service 8000:8000
```

## Verification Steps

### 1. Check Pod Status
```bash
kubectl get pods
# All pods should show Running (1/1) status
```

### 2. Verify Services
```bash
kubectl get services
# Should show both frontend and backend services
```

### 3. Test Application
- Open browser to http://localhost:3000
- Verify no CORS errors in browser console
- Test login and task creation functionality

### 4. Network Audit
```bash
# Check for any external URL calls in the application
# In browser dev tools Network tab, filter for *.vercel.app or other external domains
```

## AI Ops Features

### Using kubectl-ai
```bash
# Check pod logs using natural language
kubectl-ai "show me logs from the frontend pod"

# Troubleshoot issues with AI assistance
kubectl-ai "why is the backend restarting?"

# Get resource usage information
kubectl-ai "show me CPU and memory usage for all pods"
```

## Cleanup

### Uninstall the Application
```bash
# Remove the Helm release
helm uninstall todo-app

# Clean up any remaining resources
kubectl delete pvc --all
```

### Stop Minikube
```bash
minikube stop
```

### Clean Up Docker Images (Optional)
```bash
# Remove unused Docker images to save disk space
docker image prune -f

# Remove all unused Docker objects
docker system prune -f
```

## Troubleshooting

### Common Issues and Solutions

#### 1. Pod Status Stuck in Pending
- Check if Minikube has sufficient resources allocated
- Verify Docker images were loaded into Minikube
- Check resource limits in the Helm chart

#### 2. Service Not Accessible
- Verify service is running: `kubectl get svc`
- Check if port forwarding is needed: `kubectl port-forward`
- Ensure firewall isn't blocking the ports

#### 3. CORS Errors
- Verify auth-client.ts has localhost URLs hardcoded
- Check if backend CORS settings allow localhost:3000

#### 4. Database Connection Issues
- Confirm database secrets are properly configured
- Verify database pod is running and accessible
- Check database connection string in the application configuration