# Data Model: Phase 4: Local Kubernetes Deployment & AI Ops Integration

## System Architecture Components

### 1. Deployment Configuration
**Purpose**: Defines the structure for deploying the application to Kubernetes

**Attributes**:
- `helm_chart`: Configuration files for Kubernetes deployment
- `values`: Parameterized settings for different environments
- `templates`: Kubernetes resource definitions (Deployments, Services, ConfigMaps)
- `secrets`: Encrypted configuration for sensitive data (database passwords, API keys)

**Relationships**:
- Contains multiple Kubernetes resources
- Maps to container images defined in Docker configurations

### 2. Container Images
**Purpose**: Defines optimized Docker images for frontend and backend services

**Attributes**:
- `frontend_image`: Optimized Docker image for the React/Next.js application
- `backend_image`: Optimized Docker image for the FastAPI application
- `image_size`: Target size < 500MB per image
- `build_strategy`: Multi-stage build process

**Relationships**:
- Referenced by Kubernetes deployments in Helm charts
- Built from Dockerfiles with multi-stage optimizations

### 3. Service Definitions
**Purpose**: Kubernetes service configurations for network connectivity

**Attributes**:
- `frontend_service`: Exposes the frontend application
- `backend_service`: Exposes the backend API
- `port_mapping`: Port configuration (3000 for frontend, 8000 for backend)
- `service_type`: NodePort for frontend, ClusterIP for backend

**Relationships**:
- Connects to deployment configurations
- Enables internal and external communication

### 4. Network Security Configuration
**Purpose**: Enforces localhost-only access and prevents external URL calls

**Attributes**:
- `auth_client_config`: Hardcoded localhost URLs in auth-client.ts
- `cors_settings`: Restrictive CORS configuration
- `allowed_origins`: Limited to localhost:3000
- `api_endpoints`: Local API endpoint definitions

**Relationships**:
- Configures frontend application behavior
- Affects backend security policies

### 5. Database Connection Management
**Purpose**: Secure database connection using Kubernetes secrets

**Attributes**:
- `db_host`: Database hostname (likely within cluster)
- `db_port`: Database port (typically 5432 for PostgreSQL)
- `db_user`: Database username
- `db_password`: Encrypted database password
- `db_name`: Database name

**Relationships**:
- Referenced by backend application configuration
- Stored securely in Kubernetes secrets

## Deployment Flow

### Pre-deployment Phase
1. **Image Building**: Docker images are built with multi-stage optimization
2. **Secret Preparation**: Database credentials are prepared as Kubernetes secrets
3. **Helm Chart Configuration**: Values are customized for local deployment

### Deployment Phase
1. **Minikube Initialization**: Kubernetes cluster is started locally
2. **Image Loading**: Docker images are loaded into Minikube's registry
3. **Helm Installation**: Application is deployed using Helm charts
4. **Service Exposure**: Frontend is exposed via NodePort at localhost:3000

### Post-deployment Phase
1. **Health Verification**: All pods reach Running (1/1) status
2. **Network Validation**: No external URL requests are made
3. **Functionality Testing**: User authentication and task creation work
4. **Cleanup**: Unused Docker images are pruned to save space

## AI Ops Integration Points

### kubectl-ai Usage Patterns
- Querying pod status and logs using natural language
- Troubleshooting deployment issues with AI assistance
- Scaling services based on AI recommendations

### Monitoring Elements
- Pod health status
- Resource utilization
- Service availability
- Error rates and troubleshooting

## Storage Management Model

### Docker Image Lifecycle
- **Build**: New image creation with --no-cache option
- **Load**: Transfer to Minikube registry
- **Run**: Pod instantiation using image
- **Cleanup**: Pruning of unused images

### Disk Space Optimization
- Multi-stage builds to minimize image size
- Automated cleanup after successful deployment
- Efficient layer caching during builds