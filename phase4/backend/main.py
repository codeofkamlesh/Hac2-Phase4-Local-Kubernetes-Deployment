from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uuid
import os
from datetime import datetime
from cohere import Client as CohereClient
import cohere
from sqlmodel import Session, select

from db import create_db_and_tables, test_connection, get_session
from models import Message, Conversation, MessageRoleEnum, Task, User
from tools import (
    add_task,
    list_tasks,
    complete_task,
    delete_task,
    update_task,
    get_conversation_history,
    add_message_to_conversation
)

# System Preamble for Schema Enforcement
SYSTEM_PREAMBLE = "You are a Task Assistant. You operate on 'User', 'Task' (id, title, description, priority, completed, dueDate, userId), 'Conversation', 'Message' tables. DO NOT hallucinate columns. Use tools strictly."


def ensure_user_exists(session: Session, user_id: str) -> User:
    """
    Helper function to ensure user exists in the database.
    If user doesn't exist, creates a new user with the given ID.
    """
    user = session.get(User, user_id)
    if not user:
        print(f"🔍 User {user_id} not found in DB. Creating now...")
        new_user = User(
            id=user_id,
            email=f"{user_id}@placeholder.com",
            name="App User",
            email_verified=False,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        print(f"✅ User Created. ID: {user_id}")
        return new_user
    else:
        print(f"✅ User Found. ID: {user_id}")
        return user

import os
from dotenv import load_dotenv

load_dotenv()


# Lifespan context manager for startup events
@asynccontextmanager
async def lifespan(app: FastAPI):
    print("\n" + "="*50)
    print("🚀 Starting Todo API - Phase II with AI Backend")

    # API Key Check
    key_status = "✅ Found" if (os.getenv("COHERE_API_KEY") or os.getenv("CO_API_KEY")) else "❌ MISSING"
    print(f"🔑 Cohere API Key Check: {key_status}")

    # Test Connection
    if test_connection():
        print("✅ Database connection verified")
        # Create Tables
        create_db_and_tables()
    else:
        print("❌ Database connection failed!")

    print("="*50 + "\n")
    yield


app = FastAPI(
    title="Todo API - Phase II with AI Backend",
    version="2.0.0",
    lifespan=lifespan
)


# CORS Configuration - Fixed for Frontend Access
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://hac2-phase3-ai-powered-todo-app-wit.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Specific origins are safer/better than "*"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response models
class ChatRequest(BaseModel):
    message: str
    user_id: str
    conversation_id: Optional[str] = None


class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    timestamp: datetime


def get_cohere_client():
    api_key = os.getenv("COHERE_API_KEY") or os.getenv("CO_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="Cohere API key not configured")
    return CohereClient(api_key=api_key)


@app.post("/api/chat", response_model=ChatResponse)
async def chat_endpoint(
    request: ChatRequest,
    cohere_client: CohereClient = Depends(get_cohere_client),
    session: Session = Depends(lambda: next(get_session()))
):
    """
    Main chat endpoint that handles user messages and responds using Cohere AI.
    Implements robust Re-Act loop with schema enforcement and crash-proof design.
    """
    try:
        # Paranoid Logging Step 1: Request received
        print(f"📩 Request received from UserID: {request.user_id}")

        # Robust User Sync: Call helper function immediately at start
        user = ensure_user_exists(session, request.user_id)

        # If no conversation_id is provided, create a new conversation
        if not request.conversation_id:
            print("💾 Creating new conversation...")
            conversation_id = str(uuid.uuid4())

            # Create new conversation record
            new_conversation = Conversation(
                id=conversation_id,
                user_id=request.user_id,
                title=f"Conversation {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            )
            session.add(new_conversation)
            session.commit()
        else:
            existing_conv = session.get(Conversation, request.conversation_id)
            if not existing_conv:
                print(f"⚠️ Conversation {request.conversation_id} not found. Starting new conversation.")
                # Reset conversation_id to None so a new one is created below
                conversation_id = None
                # Create a new conversation since the old one doesn't exist
                conversation_id = str(uuid.uuid4())

                # Create new conversation record
                new_conversation = Conversation(
                    id=conversation_id,
                    user_id=request.user_id,
                    title=f"Conversation {datetime.now().strftime('%Y-%m-%d %H:%M')}"
                )
                session.add(new_conversation)
                session.commit()
            else:
                conversation_id = request.conversation_id

        # Paranoid Logging Step 4: Save user message
        print("💾 Saving User Message to DB...")
        user_message = Message(
            id=str(uuid.uuid4()),
            conversation_id=conversation_id,
            role=MessageRoleEnum.user,
            content=request.message
        )
        session.add(user_message)
        session.commit()

        # Retrieve conversation history to provide context to the AI
        raw_history = get_conversation_history(conversation_id, session) if conversation_id else []

        # Implement Aggressive History Sanitization (The Fix)
        sanitized_history = []
        for msg in raw_history:
            # CRITICAL: Force None to empty string
            content = msg["content"] if msg["content"] is not None else ""
            # Map database role values to Cohere-compatible values
            db_role = msg["role"]
            if db_role == "user":
                cohere_role = "USER"
            elif db_role == "assistant":
                cohere_role = "CHATBOT"
            else:
                cohere_role = db_role.upper()  # Default to uppercase

            sanitized_history.append({"role": cohere_role, "message": content})

        # Token Conservation: Limit to last 10 messages to save tokens
        sanitized_history = sanitized_history[-10:]

        # The user's current message is already in the database and retrieved in raw_history,
        # so we don't need to add it again. The sanitized_history already contains it.

        # Define the tools that Cohere can use
        tools = [
            {
                "name": "add_task",
                "description": "Add a new task to the user's task list",
                "parameter_definitions": {
                    "title": {
                        "description": "The title of the task",
                        "type": "str",
                        "required": True
                    },
                    "description": {
                        "description": "Optional description of the task",
                        "type": "str",
                        "required": False
                    },
                    "priority": {
                        "description": "Priority level ('high', 'medium', 'low')",
                        "type": "str",
                        "required": False,
                        "default": "medium"
                    },
                    "dueDate": {
                        "description": "Due date for the task (various formats accepted)",
                        "type": "str",
                        "required": False
                    },
                    "tags": {
                        "description": "Tags for the task (comma separated if multiple)",
                        "type": "str",
                        "required": False
                    },
                    "recurring": {
                        "description": "Recurring pattern ('daily', 'weekly', 'monthly', 'yearly')",
                        "type": "str",
                        "required": False
                    },
                    "completed": {
                        "description": "Whether the task is initially completed",
                        "type": "bool",
                        "required": False,
                        "default": False
                    }
                }
            },
            {
                "name": "list_tasks",
                "description": "List tasks for the user with optional filtering",
                "parameter_definitions": {
                    "status": {
                        "description": "Filter by status ('completed', 'pending', or None for all)",
                        "type": "str",
                        "required": False
                    },
                    "limit": {
                        "description": "Maximum number of tasks to return",
                        "type": "int",
                        "required": False,
                        "default": 10
                    }
                }
            },
            {
                "name": "complete_task",
                "description": "Mark a task as completed",
                "parameter_definitions": {
                    "task_id": {
                        "description": "ID of the task to complete",
                        "type": "str",
                        "required": True
                    }
                }
            },
            {
                "name": "delete_task",
                "description": "Delete a task from the user's list",
                "parameter_definitions": {
                    "task_id": {
                        "description": "ID of the task to delete",
                        "type": "str",
                        "required": True
                    }
                }
            },
            {
                "name": "update_task",
                "description": "Update a task with new information",
                "parameter_definitions": {
                    "task_id": {
                        "description": "ID of the task to update",
                        "type": "str",
                        "required": True
                    },
                    "updates": {
                        "description": "Dictionary of fields to update",
                        "type": "dict",
                        "required": True
                    }
                }
            }
        ]

        # Robust Re-Act Loop Implementation
        current_message = request.message
        current_tool_results = None

        # Loop (while True):
        turn_count = 0
        max_turns = 10  # Safety limit to prevent infinite loops

        while turn_count < max_turns:
            turn_count += 1
            print(f"🔄 Re-Act loop turn {turn_count}")

            # Paranoid Logging Step 5: Send to Cohere
            print("🤖 Sending request to Cohere...")

            # DEBUG: Print the sanitized history before sending to Cohere
            print(f"DEBUG: About to send clean_chat_history with {len(sanitized_history)} items:")
            for idx, hist_item in enumerate(sanitized_history):
                role = hist_item.get("role", "MISSING_ROLE")
                message = hist_item.get("message", "MISSING_MESSAGE")
                print(f"DEBUG[{idx}]: role='{role}', message='{message}', type_msg={type(message)}, is_none={message is None}")

            # Comprehensive sanitization of chat_history before sending to Cohere
            # Make a clean copy to ensure no None values
            clean_chat_history = []
            for idx, hist_item in enumerate(sanitized_history):
                # Ensure each history item has both 'role' and 'message' with safe values
                role = hist_item.get("role", "UNKNOWN")
                message = hist_item.get("message")

                if message is None:
                    print(f"DEBUG: Sanitizing None message at index {idx}, role: {role}")
                    message = " "  # Use space instead of empty string to avoid "no message" error
                elif message == "":
                    # Even empty strings might cause the error, so replace with space
                    print(f"DEBUG: Converting empty message to space at index {idx}, role: {role}")
                    message = " "

                clean_chat_history.append({
                    "role": str(role) if role is not None else "UNKNOWN",
                    "message": str(message) if message is not None else " "
                })

            # Final verification
            print(f"DEBUG: Final clean_chat_history: {clean_chat_history}")

            # Call Cohere:
            # response = cohere_client.chat(message=current_message, chat_history=sanitized_history, tool_results=current_tool_results, preamble=SYSTEM_PREAMBLE, ...)
            try:
                response = cohere_client.chat(
                    message=current_message,
                    chat_history=clean_chat_history,  # Use the completely sanitized version
                    tool_results=current_tool_results,
                    tools=tools,
                    preamble=SYSTEM_PREAMBLE,  # Pass the system preamble
                    model="command-r-08-2024",  # Using specific dated stable model
                    max_tokens=150,  # Token conservation: force concise responses
                    temperature=0.3  # Lower temperature for more consistent behavior
                )
            except (cohere.errors.NotFoundError, cohere.errors.UnauthorizedError) as e:
                print(f"⚠️ Primary model failed: {e}. Falling back to command-light...")
                # Fallback to command-light if primary model fails
                response = cohere_client.chat(
                    message=current_message,
                    chat_history=clean_chat_history,  # Use the completely sanitized version
                    tool_results=current_tool_results,
                    tools=tools,
                    preamble=SYSTEM_PREAMBLE,  # Pass the system preamble
                    model="command-light",  # Failsafe fallback model
                    max_tokens=150,  # Token conservation: force concise responses
                    temperature=0.3  # Lower temperature for more consistent behavior
                )

            # If Tools Triggered:
            if hasattr(response, 'tool_calls') and response.tool_calls:
                # Execute tools (inject user_id)
                tool_results = []

                # Add Assistant's response to history BEFORE processing tools
                # Force message to be an empty string if it's None
                assistant_msg_text = response.text if hasattr(response, 'text') and response.text else ""
                sanitized_history.append({
                    "role": "CHATBOT",
                    "message": assistant_msg_text
                })

                # Paranoid Logging Step 6: Tool execution
                print(f"🔧 Tools Triggered: {response.tool_calls}")

                for tool_call in response.tool_calls:
                    tool_name = tool_call.name
                    tool_parameters = tool_call.parameters.copy()  # Create a copy to avoid modifying original

                    # Execute the appropriate tool with user_id injection (strictly enforced)
                    if tool_name == "add_task":
                        tool_parameters["user_id"] = request.user_id  # Strictly inject user_id
                        result = add_task(session, **tool_parameters)
                    elif tool_name == "list_tasks":
                        tool_parameters["user_id"] = request.user_id  # Strictly inject user_id
                        result = list_tasks(session, **tool_parameters)
                    elif tool_name == "complete_task":
                        tool_parameters["user_id"] = request.user_id  # Strictly inject user_id
                        result = complete_task(session, **tool_parameters)
                    elif tool_name == "delete_task":
                        tool_parameters["user_id"] = request.user_id  # Strictly inject user_id
                        result = delete_task(session, **tool_parameters)
                    elif tool_name == "update_task":
                        tool_parameters["user_id"] = request.user_id  # Strictly inject user_id
                        result = update_task(session, **tool_parameters)
                    else:
                        result = {"success": False, "message": f"Unknown tool: {tool_name}"}

                    # Build the tool result in the required format
                    tool_result = {
                        'call': tool_call,
                        'outputs': [{'result': result}]
                    }
                    tool_results.append(tool_result)

                # Append to History (Local Memory):
                # Add User's tool invocation:
                sanitized_history.append({
                    "role": "USER",
                    "message": ""  # As specified in requirements
                })

                # Add Assistant's tool plan:
                sanitized_history.append({
                    "role": "CHATBOT",  # As specified in requirements
                    "message": ""  # As specified in requirements
                })

                # Prepare Next Turn:
                # current_message = ""
                # current_tool_results = tool_results_list
                current_message = ""
                current_tool_results = tool_results

                # Continue to next turn
                continue

            # If Text Response:
            if hasattr(response, 'text') and response.text and response.text.strip():
                # Add Assistant's response to sanitized history as well
                assistant_msg_text = response.text if hasattr(response, 'text') and response.text else ""
                sanitized_history.append({
                    "role": "CHATBOT",
                    "message": assistant_msg_text
                })

                # Save to DB
                print("📤 Sending Response to Client")
                ai_message = Message(
                    id=str(uuid.uuid4()),
                    conversation_id=conversation_id,
                    role=MessageRoleEnum.assistant,
                    content=assistant_msg_text
                )
                session.add(ai_message)
                session.commit()

                # Return to User
                return ChatResponse(
                    response=assistant_msg_text,
                    conversation_id=conversation_id,
                    timestamp=datetime.now()
                )

            # Break if no more processing needed
            break

        # If we somehow reach here without a text response, return a default response
        print("📤 Sending Default Response to Client")
        default_response = "Processing completed."
        ai_message = Message(
            id=str(uuid.uuid4()),
            conversation_id=conversation_id,
            role=MessageRoleEnum.assistant,
            content=default_response
        )
        session.add(ai_message)
        session.commit()

        return ChatResponse(
            response=default_response,
            conversation_id=conversation_id,
            timestamp=datetime.now()
        )

    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"❌ CRITICAL ERROR: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing chat request: {str(e)}")


@app.get("/")
def read_root():
    return {"status": "healthy", "message": "AI-Powered Todo API is Running"}


@app.get("/health")
def health_check():
    return {"status": "ok", "database": "connected", "ai_backend": "ready"}


# GET endpoint to retrieve user's conversations
@app.get("/api/conversations/{user_id}")
def get_user_conversations(user_id: str, session: Session = Depends(lambda: next(get_session()))):
    """
    Retrieve all conversations for a specific user, ordered by created_at desc.
    Returns: [{id, title, updated_at}, ...]
    """
    try:
        # Query conversations for the user, ordered by created_at descending
        statement = select(Conversation).where(Conversation.user_id == user_id).order_by(Conversation.created_at.desc())
        conversations = session.exec(statement).all()

        # Format the response
        result = []
        for conv in conversations:
            result.append({
                "id": conv.id,
                "title": conv.title,
                "updated_at": conv.created_at.isoformat() if conv.created_at else None  # Use created_at since updated_at may not exist yet
            })

        return result
    except Exception as e:
        print(f"Error retrieving conversations: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving conversations: {str(e)}")


# GET endpoint to retrieve messages for a specific conversation
@app.get("/api/conversations/{conversation_id}/messages")
def get_conversation_messages(conversation_id: str, session: Session = Depends(lambda: next(get_session()))):
    """
    Retrieve all messages for a specific conversation, ordered by created_at asc.
    Returns: [{id, role, content, created_at}, ...]
    """
    try:
        # Query messages for the conversation, ordered by created_at ascending
        messages = session.exec(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc())
        ).all()

        # Format the response
        result = []
        for msg in messages:
            result.append({
                "id": msg.id,
                "role": msg.role.value if hasattr(msg.role, 'value') else msg.role,
                "content": msg.content,
                "created_at": msg.created_at.isoformat()
            })

        return result
    except Exception as e:
        print(f"Error retrieving messages: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving messages: {str(e)}")


# Import db module (assuming it exists)
try:
    import db
except ImportError:
    # If db module doesn't exist, create a minimal version
    from sqlmodel import create_engine
    from typing import Generator

    def get_engine():
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            raise ValueError("DATABASE_URL environment variable is not set")
        return create_engine(database_url)

    def get_session():
        engine = get_engine()
        from sqlmodel import Session
        with Session(engine) as session:
            yield session