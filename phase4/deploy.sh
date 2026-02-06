#!/bin/bash

# Script to automate deployment to Minikube
# Must be run from the phase4 directory

echo "🚀 Starting deployment to Minikube..."

# Step 1: Load Images into Minikube
echo "🐳 Loading images into Minikube..."
minikube image load todo-backend:latest
minikube image load todo-frontend:latest

# Step 2: Load Secrets from .env file
echo "🔒 Loading environment variables from .env file..."
if [ -f "./backend/.env" ]; then
    source ./backend/.env
else
    echo "❌ Error: .env file not found at ./backend/.env"
    exit 1
fi

# Step 3: Helm Install/Upgrade
echo "🚀 Deploying via Helm..."
helm upgrade --install todo-app ./k8s/todo-chart \
    --set env.databaseUrl="$DATABASE_URL" \
    --set env.cohereApiKey="$COHERE_API_KEY" \
    --set env.betterAuthSecret="$BETTER_AUTH_SECRET"

# Step 4: Show Status
echo "📊 Checking deployment status..."
kubectl get pods

echo "✅ Deployment script completed!"