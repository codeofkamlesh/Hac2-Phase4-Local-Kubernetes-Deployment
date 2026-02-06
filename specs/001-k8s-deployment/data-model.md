# Data Model: Phase 4: Local Kubernetes Deployment

**Feature**: 001-k8s-deployment
**Date**: 2026-02-05
**Status**: Design

## Overview

This data model describes the configuration and deployment entities for the Kubernetes-based deployment of the Todo application. The model focuses on deployment configurations, service definitions, and infrastructure as code components rather than application data.

## Kubernetes Resources

### Backend Deployment Configuration
- **entity**: BackendDeployment
- **purpose**: Defines the FastAPI backend application deployment in Kubernetes
- **attributes**:
  - replicas: integer (default: 1, for local Minikube)
  - image: string (container image name and tag)
  - containerPort: integer (8000 for FastAPI)
  - resources.requests.memory: string (e.g., "128Mi")
  - resources.requests.cpu: string (e.g., "100m")
  - resources.limits.memory: string (e.g., "256Mi")
  - resources.limits.cpu: string (e.g., "200m")
  - env: array of environment variables
  - livenessProbe.httpGet.path: string (e.g., "/health")
  - livenessProbe.httpGet.port: integer
  - readinessProbe.httpGet.path: string (e.g., "/health")
  - readinessProbe.httpGet.port: integer

### Frontend Deployment Configuration
- **entity**: FrontendDeployment
- **purpose**: Defines the Next.js frontend application deployment in Kubernetes
- **attributes**:
  - replicas: integer (default: 1, for local Minikube)
  - image: string (container image name and tag)
  - containerPort: integer (3000 for Next.js)
  - resources.requests.memory: string (e.g., "256Mi")
  - resources.requests.cpu: string (e.g., "100m")
  - resources.limits.memory: string (e.g., "512Mi")
  - resources.limits.cpu: string (e.g., "200m")
  - env: array of environment variables
  - livenessProbe.httpGet.path: string (e.g., "/api/health")
  - livenessProbe.httpGet.port: integer
  - readinessProbe.httpGet.path: string (e.g., "/api/health")
  - readinessProbe.httpGet.port: integer

### Backend Service Configuration
- **entity**: BackendService
- **purpose**: Exposes the backend application internally within the cluster
- **attributes**:
  - name: string ("backend-service")
  - type: string ("ClusterIP")
  - port: integer (8000)
  - targetPort: integer (8000)
  - selector: object (matches backend deployment labels)

### Frontend Service Configuration
- **entity**: FrontendService
- **purpose**: Exposes the frontend application externally to users
- **attributes**:
  - name: string ("frontend-service")
  - type: string ("NodePort")
  - port: integer (80)
  - targetPort: integer (3000)
  - nodePort: integer (optional, specific port number)
  - selector: object (matches frontend deployment labels)

### Secret Configuration
- **entity**: AppSecrets
- **purpose**: Stores sensitive configuration data securely
- **attributes**:
  - databaseUrl: string (encrypted database connection string)
  - cohereApiKey: string (encrypted API key)
  - betterAuthSecret: string (encrypted auth secret)

### ConfigMap Configuration
- **entity**: AppConfigMap
- **purpose**: Stores non-sensitive configuration data
- **attributes**:
  - nextPublicApiUrl: string (backend API URL for frontend)
  - environment: string (development/local/production)

## Helm Chart Values

### Chart Configuration
- **entity**: HelmValues
- **purpose**: Defines configurable parameters for the Helm chart
- **attributes**:
  - backend.image.repository: string (backend container image repository)
  - backend.image.tag: string (backend container image tag)
  - backend.service.type: string (service type for backend)
  - backend.service.port: integer (port for backend service)
  - backend.resources.requests.memory: string (memory request for backend)
  - backend.resources.limits.memory: string (memory limit for backend)
  - frontend.image.repository: string (frontend container image repository)
  - frontend.image.tag: string (frontend container image tag)
  - frontend.service.type: string (service type for frontend)
  - frontend.service.port: integer (port for frontend service)
  - frontend.resources.requests.memory: string (memory request for frontend)
  - frontend.resources.limits.memory: string (memory limit for frontend)
  - ingress.enabled: boolean (whether to enable ingress)
  - ingress.hosts: array of host configurations

## Relationships

### Deployment to Service Relationship
- BackendDeployment → BackendService (via selector labels)
- FrontendDeployment → FrontendService (via selector labels)

### Configuration Dependencies
- BackendDeployment → AppSecrets (for database URL and API keys)
- BackendDeployment → AppConfigMap (for environment configuration)
- FrontendDeployment → AppConfigMap (for API URL configuration)

## Constraints

### Resource Constraints
- Memory requests should be less than limits
- CPU requests should not exceed node capacity
- NodePort should be within valid range (30000-32767)

### Security Constraints
- Sensitive data must be stored in Secrets, not ConfigMaps
- Database URLs should not be exposed in logs or accessible to clients

## Validation Rules

### Deployment Validation
- Replicas count must be non-negative
- Container port must be valid (1-65535)
- Image must be specified

### Service Validation
- Service type must be valid (ClusterIP, NodePort, LoadBalancer)
- Port numbers must be valid (1-65535)
- Target ports must match container ports in deployment

## State Transitions

### Deployment Lifecycle
- Pending → Running → Terminating → Deleted (standard Kubernetes states)
- Healthy → Unhealthy → Restarting (based on probe results)