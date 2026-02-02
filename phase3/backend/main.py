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
    Integrates with MCP tools for task operations.
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
        conversation_history = get_conversation_history(conversation_id, session)

        # Prepare the chat history for Cohere
        chat_history = []
        for msg in conversation_history:
            chat_history.append({
                "role": msg["role"],
                "message": msg["content"]
            })

        # Token Conservation: Limit to last 10 messages to save tokens
        chat_history = chat_history[-10:]

        # Add the user's current message to the chat history
        chat_history.append({
            "role": "USER",
            "message": request.message
        })

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

        # Multi-Step Tool Execution Loop (Re-Act: Reason + Act)
        turn_count = 0
        max_turns = 5  # Safety limit to prevent infinite loops
        ai_response = ""

        while turn_count < max_turns:
            turn_count += 1
            print(f"🔄 Multi-step loop turn {turn_count}")

            # Paranoid Logging Step 5: Send to Cohere
            print("🤖 Sending request to Cohere...")

            # Call Cohere with tools - using specific dated model with fallback
            try:
                response = cohere_client.chat(
                    message="",  # Empty string for subsequent turns to process tool results
                    chat_history=chat_history,
                    tools=tools,
                    model="command-r-08-2024",  # Using specific dated stable model
                    max_tokens=150  # Token conservation: force concise responses
                )
            except (cohere.errors.NotFoundError, cohere.errors.UnauthorizedError) as e:
                print(f"⚠️ Primary model failed: {e}. Falling back to command-light...")
                # Fallback to command-light if primary model fails
                response = cohere_client.chat(
                    message="",  # Empty string for subsequent turns to process tool results
                    chat_history=chat_history,
                    tools=tools,
                    model="command-light",  # Failsafe fallback model
                    max_tokens=150  # Token conservation: force concise responses
                )

            # Check if there are tool calls
            if hasattr(response, 'tool_calls') and response.tool_calls:
                # Implement Strict Task Guardrails (The "3 Task Limit")
                add_task_calls = [t for t in response.tool_calls if t.name == 'add_task']
                if len(add_task_calls) > 3:
                    # REJECT the request to save resources
                    return ChatResponse(
                        response="⚠️ Limit Reached: I can only add up to 3 tasks at a time to save resources. Please break your request into smaller parts.",
                        conversation_id=conversation_id,
                        timestamp=datetime.now()
                    )

                # Process tool calls
                for tool_call in response.tool_calls:
                    tool_name = tool_call.name
                    tool_parameters = tool_call.parameters.copy()  # Create a copy to avoid modifying original

                    # Paranoid Logging Step 6: Tool execution
                    print(f"🔧 Tool Triggered: {tool_name} with Params: {tool_parameters}")

                    # Execute the appropriate tool with user_id injection
                    if tool_name == "add_task":
                        tool_parameters["user_id"] = request.user_id  # <--- Inject this!
                        result = add_task(session, **tool_parameters)
                    elif tool_name == "list_tasks":
                        tool_parameters["user_id"] = request.user_id  # <--- Inject this!
                        result = list_tasks(session, **tool_parameters)
                    elif tool_name == "complete_task":
                        tool_parameters["user_id"] = request.user_id  # <--- Inject this!
                        result = complete_task(session, **tool_parameters)
                    elif tool_name == "delete_task":
                        tool_parameters["user_id"] = request.user_id  # <--- Inject this!
                        result = delete_task(session, **tool_parameters)
                    elif tool_name == "update_task":
                        tool_parameters["user_id"] = request.user_id  # <--- Inject this!
                        result = update_task(session, **tool_parameters)
                    else:
                        result = {"success": False, "message": f"Unknown tool: {tool_name}"}

                    # Add tool result to chat for follow-up
                    tool_result_msg = f"Tool result: {result.get('message', str(result))}"

                    # Append the tool result to chat_history so the AI knows what happened
                    chat_history.append({
                        "role": "TOOL",
                        "message": tool_result_msg
                    })

                    # Add to final response
                    ai_response += f"\n{tool_result_msg}"

                # Continue the loop to let the AI decide on next steps
                continue

            # If no tool calls, check for text response and break the loop
            else:
                if hasattr(response, 'text') and response.text:
                    ai_response += f"\n{response.text}"

                # Break the loop since there are no more tools to execute
                break

        # If we reached max turns without breaking naturally
        if turn_count >= max_turns:
            print(f"⚠️ Reached maximum turns ({max_turns}) in multi-step loop")
            ai_response += f"\n⚠️ Maximum processing steps reached. Some actions may be incomplete."

        # Add AI response to conversation
        print("📤 Sending Response to Client")
        ai_message = Message(
            id=str(uuid.uuid4()),
            conversation_id=conversation_id,
            role=MessageRoleEnum.assistant,
            content=ai_response
        )
        session.add(ai_message)
        session.commit()

        return ChatResponse(
            response=ai_response,
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