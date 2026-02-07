# API Contract: Todo Chatbot Application

## Overview
This document defines the API contracts for the Todo Chatbot application deployed in the local Kubernetes environment.

## Base URLs
- **Local Development**: `http://localhost:8000/api`
- **Internal Service (within cluster)**: `http://todo-backend-service:8000/api`

## Authentication API

### POST /auth/signup
**Description**: Register a new user account
**Headers**:
- `Content-Type: application/json`
- `Origin: http://localhost:3000` (for CORS validation)

**Request Body**:
```json
{
  "email": "string",
  "password": "string",
  "name": "string"
}
```

**Response Codes**:
- `201`: User created successfully
- `400`: Invalid input data
- `409`: Email already exists

### POST /auth/signin
**Description**: Authenticate a user
**Headers**:
- `Content-Type: application/json`
- `Origin: http://localhost:3000` (for CORS validation)

**Request Body**:
```json
{
  "email": "string",
  "password": "string"
}
```

**Response Codes**:
- `200`: Authentication successful
- `400`: Invalid input data
- `401`: Invalid credentials

## Todo Management API

### GET /todos
**Description**: Retrieve all todos for authenticated user
**Headers**:
- `Authorization: Bearer {token}`
- `Origin: http://localhost:3000` (for CORS validation)

**Response Codes**:
- `200`: Todos retrieved successfully
- `401`: Unauthorized access

### POST /todos
**Description**: Create a new todo
**Headers**:
- `Content-Type: application/json`
- `Authorization: Bearer {token}`
- `Origin: http://localhost:3000` (for CORS validation)

**Request Body**:
```json
{
  "title": "string",
  "description": "string",
  "due_date": "string" // ISO 8601 format
}
```

**Response Codes**:
- `201`: Todo created successfully
- `400`: Invalid input data
- `401`: Unauthorized access

## AI Integration API

### POST /ai/process-task
**Description**: Process a natural language task using AI
**Headers**:
- `Content-Type: application/json`
- `Authorization: Bearer {token}`
- `Origin: http://localhost:3000` (for CORS validation)

**Request Body**:
```json
{
  "task_description": "string"
}
```

**Response Codes**:
- `200`: AI processed task successfully
- `400`: Invalid input data
- `401`: Unauthorized access
- `500`: AI service error

## Internal Service Contracts

### Database Connectivity Contract
- **Service**: PostgreSQL database
- **Connection**: Via Kubernetes DNS: `postgres-service.default.svc.cluster.local:5432`
- **Credentials**: Provided via Kubernetes secrets

### AI Service Contract
- **Service**: Cohere API (local proxy if needed)
- **Connection**: Configured via environment variables in deployment
- **Authentication**: API key via Kubernetes secrets