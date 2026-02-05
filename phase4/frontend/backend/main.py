from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Absolute imports instead of relative
from db import get_session, create_db_and_tables
from models import Message, Conversation, MessageRoleEnum
from tools import get_conversation_history, add_message_to_conversation
from agent import run_agent


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    create_db_and_tables()
    yield
    # Shutdown


app = FastAPI(
    title="Todo App AI Backend",
    description="AI-powered backend for the Todo App with Cohere integration",
    version="1.0.0",
    lifespan=lifespan
)


# Add CORS middleware to allow requests from Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
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


@app.post("/api/chat")
async def chat_endpoint(
    request: ChatRequest,
    session=Depends(get_session)
):
    """
    Main chat endpoint that handles user messages and responds using Cohere AI.
    Integrates with tools for task operations.
    """
    try:
        # If no conversation_id is provided, create a new conversation
        if not request.conversation_id:
            conversation_id = str(uuid.uuid4())

            # Create new conversation record
            new_conversation = Conversation(
                id=conversation_id,
                user_id=request.user_id,
                title=f"Conversation {datetime.now().strftime('%Y-%m-%d %H:%M')}",
                created_at=datetime.utcnow()
            )
            session.add(new_conversation)
            session.commit()
            session.refresh(new_conversation)
        else:
            conversation_id = request.conversation_id

        # Add user message to conversation
        user_message_added = add_message_to_conversation(
            conversation_id,
            "user",
            request.message,
            session
        )

        if not user_message_added:
            raise HTTPException(status_code=500, detail="Failed to add user message to conversation")

        # Retrieve conversation history to provide context to the AI
        conversation_history = get_conversation_history(conversation_id, session)

        # Process the message through the AI agent
        ai_response = run_agent(
            request.message,
            conversation_history,
            request.user_id,
            session
        )

        # Add AI response to conversation
        ai_message_added = add_message_to_conversation(
            conversation_id,
            "assistant",
            ai_response,
            session
        )

        if not ai_message_added:
            raise HTTPException(status_code=500, detail="Failed to add AI response to conversation")

        return {
            "response": ai_response,
            "conversation_id": conversation_id,
            "timestamp": datetime.utcnow()
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing chat request: {str(e)}")


@app.get("/")
def read_root():
    return {"status": "healthy", "message": "AI-Powered Todo API is Running"}


@app.get("/health")
def health_check():
    return {"status": "ok", "database": "connected", "ai_backend": "ready"}