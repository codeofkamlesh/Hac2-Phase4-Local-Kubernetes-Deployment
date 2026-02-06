# API Contract: Todo App Service Communication

**Contract ID**: api-contract-todo-v1
**Feature**: 001-k8s-deployment
**Date**: 2026-02-05
**Status**: Design

## Purpose

Defines the API contracts between frontend and backend services when deployed in Kubernetes environment.

## Base URL Patterns

### In Kubernetes Cluster
- **Backend Service URL**: `http://backend-service:8000/api/{user_id}/`
- **Frontend Service URL**: `http://frontend-service:3000` (externally accessible via NodePort)

## API Endpoints

### Authentication Endpoints
```
POST /api/auth/signup
Content-Type: application/json
Authorization: none (initial registration)

Request:
{
  "email": "user@example.com",
  "password": "secure_password_123",
  "name": "John Doe"
}

Response (201):
{
  "token": "jwt_token_here",
  "user": {
    "id": "uuid_string",
    "email": "user@example.com",
    "name": "John Doe"
  },
  "message": "Account created successfully"
}
```

```
POST /api/auth/login
Content-Type: application/json
Authorization: none (initial authentication)

Request:
{
  "email": "user@example.com",
  "password": "secure_password_123"
}

Response (200):
{
  "token": "jwt_token_here",
  "user": {
    "id": "uuid_string",
    "email": "user@example.com",
    "name": "John Doe"
  },
  "message": "Login successful"
}
```

### Task Management Endpoints

```
GET /api/{user_id}/tasks
Authorization: Bearer {jwt_token}

Response (200):
[
  {
    "id": 1,
    "user_id": "uuid_string",
    "title": "Sample task",
    "description": "Task description",
    "completed": false,
    "priority": "medium",
    "tags": ["work"],
    "due_date": "2024-12-31T00:00:00",
    "recurring": false,
    "recurrence_pattern": null,
    "created_at": "2024-01-01T00:00:00",
    "updated_at": "2024-01-01T00:00:00"
  }
]
```

```
POST /api/{user_id}/tasks
Content-Type: application/json
Authorization: Bearer {jwt_token}

Request:
{
  "title": "New task",
  "description": "Task description",
  "priority": "high",
  "tags": ["personal"],
  "due_date": "2024-12-31",
  "recurring": false,
  "recurrence_pattern": "weekly"
}

Response (201):
{
  "id": 2,
  "user_id": "uuid_string",
  "title": "New task",
  "description": "Task description",
  "completed": false,
  "priority": "high",
  "tags": ["personal"],
  "due_date": "2024-12-31T00:00:00",
  "recurring": false,
  "recurrence_pattern": "weekly",
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:00"
}
```

```
PUT /api/{user_id}/tasks/{task_id}
Content-Type: application/json
Authorization: Bearer {jwt_token}

Request:
{
  "title": "Updated task title",
  "completed": true
}

Response (200):
{
  "id": 2,
  "user_id": "uuid_string",
  "title": "Updated task title",
  "description": "Task description",
  "completed": true,
  "priority": "high",
  "tags": ["personal"],
  "due_date": "2024-12-31T00:00:00",
  "recurring": false,
  "recurrence_pattern": "weekly",
  "created_at": "2024-01-01T00:00:00",
  "updated_at": "2024-01-01T00:00:01"
}
```

### Health Check Endpoints

```
GET /health
Authorization: none

Response (200):
{
  "status": "ok",
  "database": "connected",
  "ai_backend": "ready"
}
```

```
GET /
Authorization: none

Response (200):
{
  "status": "healthy",
  "message": "AI-Powered Todo API is Running"
}
```

## Kubernetes Service Communication Contract

### Internal Service URLs
- **Backend Service**: `http://backend-service:8000`
- **Frontend Service**: `http://frontend-service:3000`

### Environment Variables for Communication
- `BACKEND_SERVICE_URL=http://backend-service:8000`
- `NEXT_PUBLIC_API_URL=http://frontend-service:3000/api` (or appropriate NodePort)

## Security Requirements

### Authentication Flow
1. Frontend makes auth request to backend via internal service URL
2. Backend generates JWT and returns to frontend
3. Subsequent requests include Authorization header with Bearer token
4. Backend verifies user_id in token matches the requested user_id in URL

### User Isolation
- All data access filtered by `user_id`
- 403 Forbidden returned for mismatched user_id requests
- JWT token must contain valid `user_id` matching URL parameter

## Error Handling

### Standard Error Response Format
```
{
  "detail": "Descriptive error message"
}
```

### Common HTTP Status Codes
- 200: Success for GET, PUT operations
- 201: Created for POST operations
- 400: Bad Request for invalid input
- 401: Unauthorized for missing/invalid token
- 403: Forbidden for user_id mismatch
- 404: Not Found for missing resources
- 500: Internal Server Error for system errors

## Kubernetes-Specific Considerations

### Service Discovery
- Backend service accessed via DNS name `backend-service`
- Port numbers must match service definitions
- Health checks used for pod readiness

### Configuration Management
- Database URL provided via Kubernetes Secrets
- API keys provided via Kubernetes Secrets
- Service URLs configured via ConfigMaps or environment variables