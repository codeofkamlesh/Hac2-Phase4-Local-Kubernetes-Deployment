# K8s Port Forward

## Description
Clears old processes and forwards the frontend service port to localhost:3000.

## Command
pkill -f 'port-forward' || true && kubectl port-forward svc/todo-frontend-service 3000:3000 --address 0.0.0.0