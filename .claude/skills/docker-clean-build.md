# Docker Clean Build

## Description
Builds frontend and backend images with --no-cache and loads them into Minikube.

## Command
docker build --no-cache -t todo-backend:latest ./backend && docker build --no-cache -t todo-frontend:latest ./frontend && minikube image load todo-backend:latest && minikube image load todo-frontend:latest