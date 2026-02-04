# Feature Specification: Phase 3 AI Backend - Chat History Persistence & Recurrence Fix

**Feature Branch**: `007-ai-backend-chat-history-persistence`
**Created**: 2026-02-04
**Status**: Draft
**Input**: User description: "Update the project specification to perfectly match the current, finished codebase of Phase 3. The backend now implements proper chat history persistence, recurrence pattern fixes, and updated data models."

## Summary

This specification documents the current implementation of the AI-powered Todo App backend which now includes comprehensive chat history persistence, proper recurrence pattern handling, and updated data models. The system leverages FastAPI, SQLModel, Cohere AI, and maintains compatibility with the existing Next.js frontend and Neon PostgreSQL database.

## User Scenarios & Testing *(mandatory)*

### User Scenario 1 - Persistent Chat History Access (Priority: P1)
As a user of the Todo App, I want my chat history to persist across page refreshes so that I can continue conversations with the AI assistant without losing context.

**Why this priority**: This is essential for a seamless user experience in an AI-powered chat interface.

**Independent Test**: User navigates away and back to the app → Previous conversation history is available → User can continue from where they left off.

**Acceptance Scenarios**:
1. **Given** user has participated in a conversation, **When** page is refreshed, **Then** conversation history remains accessible via GET /api/conversations/{user_id}
2. **Given** user selects a past conversation, **When** requesting messages, **Then** all messages in chronological order are returned via GET /api/conversations/{conversation_id}/messages
3. **Given** user has multiple conversations, **When** viewing conversation list, **Then** conversations are ordered by recency and accessible

### User Scenario 2 - Proper Recurrence Pattern Handling (Priority: P1)
As a user, I want to create recurring tasks through the AI assistant so that I can schedule repeating tasks with the correct recurrence patterns stored in the database.

**Why this priority**: Recurring tasks are a critical feature for a productivity application and must work correctly with the AI interface.

**Independent Test**: User says "Make task 'Weekly Meeting' repeat weekly" → AI creates task with proper recurrencePattern and recurring boolean set → Task appears correctly in dashboard.

**Acceptance Scenarios**:
1. **Given** user requests recurring task creation, **When** AI processes request, **Then** task is created with recurrencePattern set and recurring boolean = true
2. **Given** user updates task to recurring, **When** AI processes update, **Then** recurrencePattern is updated and recurring boolean is set to true
3. **Given** AI receives various recurrence terms ('repeat', 'frequency', 'pattern'), **When** processing, **Then** all map to the correct recurrencePattern column

### User Scenario 3 - Robust Task Operations with AI (Priority: P1)
As a user, I want to perform all task operations (create, update, complete, delete) through natural language with the AI assistant so that I can manage my tasks efficiently.

**Why this priority**: This provides the core AI-powered task management functionality.

**Independent Test**: User interacts with AI using natural language → AI correctly interprets intent → Appropriate task operations are executed with proper database schema compliance.

**Acceptance Scenarios**:
1. **Given** user provides task details in natural language, **When** AI processes request, **Then** task is created with all attributes (title, description, priority, due date, tags, recurrence) properly mapped
2. **Given** user wants to update task attributes, **When** AI processes update request, **Then** all attributes are updated using correct column mappings
3. **Given** user references tasks by title or ID, **When** AI resolves identifiers, **Then** correct tasks are operated on regardless of reference method

### Edge Cases
- What happens when a user provides ambiguous task titles that could match multiple tasks?
- How does the system handle natural language date parsing for due dates?
- What occurs when recurrence patterns are specified in various formats ('daily', 'every day', 'each day')?
- How does the system handle large conversation histories efficiently?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide GET /api/conversations/{user_id} endpoint returning user's conversations ordered by created_at desc
- **FR-002**: System MUST provide GET /api/conversations/{conversation_id}/messages endpoint returning messages ordered by created_at asc
- **FR-003**: System MUST store recurrence information using recurrencePattern (text) and recurring (boolean) columns in the Task table
- **FR-004**: System MUST map AI recurrence terms ('repeat', 'frequency', 'pattern', 'recurring') to the recurrencePattern column
- **FR-005**: System MUST set the recurring boolean flag to true when a recurrence pattern is specified
- **FR-006**: System MUST maintain backward compatibility with recurringInterval column (now deprecated)
- **FR-007**: System MUST implement smart date parsing using python-dateutil for dueDate parameters
- **FR-008**: System MUST resolve task identifiers using both numeric IDs and title strings via resolve_task_id helper
- **FR-009**: System MUST handle parameter normalization mapping AI variations to correct schema columns
- **FR-010**: System MUST maintain proper user isolation ensuring users only access their own data
- **FR-011**: System MUST implement proper error handling with graceful degradation for invalid inputs
- **FR-012**: System MUST store conversation history with proper user_id association and message ordering
- **FR-013**: System MUST integrate with Cohere API for natural language processing and tool execution
- **FR-014**: System MUST execute MCP tools with proper user_id injection for security
- **FR-015**: System MUST implement CORS configuration allowing access from Vercel frontend and local development
- **FR-016**: System MUST maintain data integrity during AI-driven database operations
- **FR-017**: System MUST return consistent JSON responses compatible with frontend expectations
- **FR-018**: System MUST handle concurrent users and conversations without data crossover
- **FR-019**: System MUST implement proper session management and database transaction handling
- **FR-020**: System MUST provide health check endpoints for monitoring and deployment

### Key Entities

- **Task**: Represents a user's task with properties (id, title, description, completed, priority, tags, dueDate, recurring, recurrencePattern, createdAt, updatedAt) mapped to camelCase columns in the database
- **User**: Represents a registered user with properties (id, name, email, emailVerified, createdAt, updatedAt) mapped to camelCase columns in the database
- **Conversation**: Represents a single AI conversation thread with properties (id, userId, title, createdAt) using camelCase mapping
- **Message**: Represents a single message within a conversation with properties (id, conversationId, role, content, createdAt) using camelCase mapping
- **MCP Tool**: Represents executable functions (add_task, list_tasks, complete_task, delete_task, update_task) with schema-compliant parameters accessible to the AI model
- **AI Assistant**: Represents the Cohere-powered agent that processes natural language and executes tools while maintaining schema compliance

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can access chat history across page refreshes with 99% reliability
- **SC-002**: Recurring tasks created via AI appear with correct recurrencePattern and recurring flags set (100% accuracy)
- **SC-003**: Task operations initiated by AI complete within 3 seconds for 95% of requests
- **SC-004**: System supports 100+ concurrent conversations without data crossover
- **SC-005**: AI correctly maps recurrence terms to proper database columns 98% of the time
- **SC-006**: Date parsing handles natural language formats with 95% success rate
- **SC-007**: Task identifier resolution works for both numeric IDs and title strings with 99% accuracy
- **SC-008**: Conversation history retrieval returns messages in correct chronological order (100% accuracy)
- **SC-009**: User isolation is maintained with 100% accuracy across all operations
- **SC-010**: System maintains 99% uptime during normal operation with proper error handling

### Quality Attributes

- **Reliability**: AI operations do not corrupt existing data or disrupt manual task management while maintaining schema compliance
- **Performance**: Natural language processing and database operations complete within acceptable timeframes with proper schema mapping
- **Security**: Proper authentication and authorization for database access through AI tools with user isolation
- **Compatibility**: Seamless integration with existing Next.js frontend and camelCase database schema
- **Scalability**: System can handle increasing number of users and conversations while maintaining performance
- **Maintainability**: Clear separation of concerns with proper API design and documentation

## Assumptions

- The existing database schema with camelCase columns is stable and documented
- Cohere API access is properly configured with appropriate credentials (COHERE_API_KEY)
- The Python FastAPI backend will run on port 8000 without conflicts
- The existing Next.js frontend communicates with the backend via CORS-enabled endpoints
- Users are authenticated through the existing Better Auth system with user_id provided in requests
- Network connectivity between frontend, backend, and Cohere API is stable
- The existing task table has columns: id, userId, title, description, completed, priority, tags, dueDate, recurring, recurrencePattern, recurringInterval, createdAt, updatedAt
- Deployment architecture uses Vercel for frontend and Hugging Face Docker for backend

## Constraints

- Must maintain backward compatibility with existing manual task management
- Database schema uses camelCase column names mapped from Python snake_case attributes via sa_column
- Implementation must follow MCP (Model Context Protocol) standards for AI tool integration
- Must use SQLModel ORM with proper sa_column_kwargs for camelCase column mapping
- Solution must be deployed separately from Next.js frontend with proper CORS configuration
- All Python snake_case attributes must map correctly to database camelCase columns
- Recurring task functionality must use both recurrencePattern (text) and recurring (boolean) columns
- Conversation and Message tables use camelCase naming convention consistent with existing schema
- All AI tool parameters must be normalized to match database schema requirements