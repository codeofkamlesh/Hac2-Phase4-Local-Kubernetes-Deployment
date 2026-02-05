# Feature Specification: Phase 3 AI Backend with Cohere & MCP (Schema Strict)

**Feature Branch**: `006-ai-backend-schema-strict`
**Created**: 2026-02-02
**Status**: Draft
**Input**: User description: "Phase 3: AI Backend with Cohere & MCP (Schema Strict) - Implement Python FastAPI backend with proper CamelCase column mapping using SQLModel."

## Summary

This specification outlines the implementation of a Python FastAPI backend for the AI-powered Todo App with strict adherence to the existing database schema. The system will use SQLModel to map Python's snake_case attributes to the database's camelCase column names, ensuring seamless integration with the existing Next.js frontend and Neon PostgreSQL database.

## User Scenarios & Testing *(mandatory)*

### User Scenario 1 - AI Task Creation with Schema Compliance (Priority: P1)
As a user of the Todo App, I want to interact with an AI assistant to create tasks using natural language so that I can quickly add tasks without navigating through forms, while ensuring all data is stored using the correct database schema.

**Why this priority**: This is the core functionality that demonstrates the schema compliance while providing AI value.

**Independent Test**: User says "Add a task to buy milk" → AI backend adds task to database using proper camelCase mapping → Task appears in dashboard after refresh.

**Acceptance Scenarios**:
1. **Given** user types "Add a task to buy milk", **When** AI processes the request, **Then** a new task with title "buy milk" is created with proper camelCase column mapping
2. **Given** user provides additional details like "Add a high priority task to buy milk tomorrow", **When** AI processes the request, **Then** task is created with appropriate priority and due date using correct schema mapping
3. **Given** user says "Create a task to call John about project", **When** AI processes the request, **Then** task is created with title "call John about project" using proper column mappings

### User Scenario 2 - AI Task Management with Schema Integrity (Priority: P1)
As a user, I want to manage my tasks through natural language conversations with the AI so that I can complete, update, or list tasks without manual interaction, while maintaining database schema integrity.

**Why this priority**: This provides comprehensive task management capabilities while ensuring schema compliance.

**Independent Test**: User says "Mark 'buy milk' as complete" → AI backend updates task status using proper camelCase mapping → Change reflects in dashboard.

**Acceptance Scenarios**:
1. **Given** user has tasks in their list, **When** user asks "What are my tasks?", **Then** AI retrieves and presents the user's tasks using correct schema mappings
2. **Given** user wants to update a task, **When** user says "Change 'buy milk' to 'buy groceries'", **Then** task title is updated in the database using proper column mapping
3. **Given** user wants to complete a task, **When** user says "Complete 'buy milk'", **Then** task status is updated to completed using correct schema mapping

### User Scenario 3 - Conversation Context with Schema Compliance (Priority: P2)
As a user, I want the AI to maintain context across my conversation so that I can have natural, flowing interactions without repetition, while ensuring all conversation data uses proper schema mappings.

**Why this priority**: This enhances user experience while maintaining database schema compliance for conversation data.

**Independent Test**: User engages in multi-turn conversation with AI → AI maintains context and stores conversation using proper camelCase column mappings.

**Acceptance Scenarios**:
1. **Given** user starts a conversation, **When** multiple exchanges occur, **Then** AI maintains context of the conversation and stores messages using correct schema
2. **Given** user refers to previous tasks in conversation, **When** AI processes the reference, **Then** AI correctly identifies and acts on the referenced task using proper mappings

### Edge Cases
- What happens when a user provides ambiguous task details that require schema validation?
- How does the system handle requests for non-existent tasks with strict schema enforcement?
- What occurs when database operations fail during AI processing with schema constraints?
- How does the system handle multiple simultaneous conversations with schema compliance?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST use SQLModel ORM with proper sa_column mapping to connect to existing Neon PostgreSQL database
- **FR-002**: System MUST map Python snake_case attributes to database camelCase columns using sa_column_kwargs
- **FR-003**: System MUST implement a `User` model that maps to existing user table with correct column mapping (email_verified -> emailVerified)
- **FR-004**: System MUST implement a `Task` model that maps to existing task table with correct column mapping:
  - user_id -> userId
  - due_date -> dueDate
  - created_at -> createdAt
  - updated_at -> updatedAt
  - recurring_interval -> recurrencePattern (or recurringInterval depending on schema)
- **FR-005**: System MUST create a `Conversation` model with id, userId, title, and createdAt fields using proper camelCase mapping
- **FR-006**: System MUST create a `Message` model with id, conversationId, role, content, and createdAt fields using proper camelCase mapping
- **FR-007**: System MUST implement an MCP server exposing `add_task` tool with parameters (title, description, priority) using proper schema mapping
- **FR-008**: System MUST implement an MCP server exposing `list_tasks` tool with parameters (status, limit) respecting database schema
- **FR-009**: System MUST implement an MCP server exposing `complete_task` tool with parameter (task_id) using correct schema mapping
- **FR-010**: System MUST implement an MCP server exposing `delete_task` tool with parameter (task_id) using correct schema mapping
- **FR-011**: System MUST implement an MCP server exposing `update_task` tool with parameters (task_id, updates) respecting schema constraints
- **FR-012**: System MUST implement a `POST /api/chat` endpoint that accepts message and userId using proper data validation
- **FR-013**: System MUST integrate with Cohere API for natural language processing and tool use while maintaining schema compliance
- **FR-014**: System MUST retrieve conversation history from the database using correct schema mappings
- **FR-015**: System MUST store both user messages and AI responses in the Message table using proper camelCase column mapping
- **FR-016**: System MUST execute MCP tools when Cohere determines appropriate actions using correct database schema
- **FR-017**: System MUST feed tool execution results back to Cohere for response generation while maintaining data integrity
- **FR-018**: System MUST implement CORS to allow access from localhost:3000 (Next.js frontend) with proper security
- **FR-019**: System MUST maintain data integrity and schema compliance during AI-driven database operations
- **FR-020**: System MUST handle errors gracefully and provide appropriate user feedback while preserving schema integrity

### Key Entities

- **Task**: Represents a user's task with properties (id, title, description, status, priority, etc.) mapped to camelCase columns in the shared database
- **User**: Represents a registered user with properties (id, name, email, etc.) mapped to camelCase columns in the shared database
- **Conversation**: Represents a single AI conversation thread with properties (id, userId, title, createdAt) using camelCase mapping
- **Message**: Represents a single message within a conversation with properties (id, conversationId, role, content, createdAt) using camelCase mapping
- **MCP Tool**: Represents an executable function (add_task, list_tasks, etc.) accessible to the AI model with schema-compliant parameters
- **AI Assistant**: Represents the Cohere-powered agent that processes natural language and executes tools while maintaining schema compliance

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can create tasks through AI assistant with 95% accuracy in interpretation while maintaining schema compliance
- **SC-002**: AI response time is under 3 seconds for 90% of requests with proper schema operations
- **SC-003**: Task operations initiated by AI appear in the dashboard within 1 refresh cycle using correct schema mapping
- **SC-004**: System supports concurrent AI conversations for multiple users without schema conflicts
- **SC-005**: AI correctly identifies and executes appropriate tools based on user requests 90% of the time while maintaining schema compliance
- **SC-006**: No data loss or schema corruption occurs in the existing task table during AI operations
- **SC-007**: Manual tasks created via dashboard remain accessible to the AI assistant with proper schema mapping
- **SC-008**: System maintains 99% uptime during peak usage hours with schema-compliant operations

### Quality Attributes

- **Reliability**: AI operations do not corrupt existing data or disrupt manual task management while maintaining schema compliance
- **Performance**: Natural language processing and database operations complete within acceptable timeframes with proper schema mapping
- **Security**: Proper authentication and authorization for database access through AI tools with schema integrity
- **Compatibility**: Seamless integration with existing Next.js frontend and camelCase database schema
- **Scalability**: System can handle increasing number of users and conversations while maintaining schema compliance

## Assumptions

- The existing database schema with camelCase columns is stable and documented
- Cohere API access is properly configured with appropriate credentials
- The Python FastAPI backend will run on port 8000 without conflicts
- The existing Next.js frontend will be updated to communicate with the new backend
- Users are authenticated through the existing Better Auth system
- Network connectivity between frontend, backend, and Cohere API is stable
- The existing task table has columns: id, userId, title, description, completed, priority, tags, dueDate, createdAt, updatedAt, recurringInterval

## Constraints

- Must maintain backward compatibility with existing manual task management
- Database schema changes are limited to new tables (Conversation, Message) - no changes to existing tables
- Implementation must follow MCP (Model Context Protocol) standards
- Must use SQLModel ORM with proper sa_column_kwargs for camelCase column mapping
- Solution must be deployed separately from Next.js frontend
- All Python snake_case attributes must map correctly to database camelCase columns

## Open Questions

- [NEEDS CLARIFICATION: What is the exact column name for recurring interval in the existing task table - is it recurringInterval or recurrencePattern?]
- [NEEDS CLARIFICATION: Are there any additional camelCase columns in the existing task table that need to be mapped?]
- [NEEDS CLARIFICATION: Should the new Conversation and Message tables use the same camelCase naming convention as the existing tables?]