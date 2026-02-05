from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum
from sqlalchemy import Column, String, Boolean, DateTime, Integer
import uuid


# Priority Enum
class PriorityEnum(str, Enum):
    high = "high"
    medium = "medium"
    low = "low"


# User Model - Maps to existing Better Auth user table
class User(SQLModel, table=True):
    __tablename__ = "user"  # Singular table name to match existing Better Auth table

    # Use sa_column to map snake_case attributes to camelCase DB columns
    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True,
        sa_column=Column("id", String, primary_key=True)
    )
    name: Optional[str] = Field(
        default=None,
        sa_column=Column("name", String)
    )
    email: str = Field(
        sa_column=Column("email", String, nullable=False, unique=True)
    )
    email_verified: bool = Field(
        default=False,
        sa_column=Column("emailVerified", Boolean, nullable=False, default=False)
    )
    image: Optional[str] = Field(
        default=None,
        sa_column=Column("image", String)
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column("createdAt", DateTime, nullable=False)
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column("updatedAt", DateTime, nullable=False)
    )


# Task Model - Maps to existing task table
class Task(SQLModel, table=True):
    __tablename__ = "task"  # Singular table name to match existing table

    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        sa_column=Column("id", Integer, primary_key=True)  # SERIAL for auto-increment
    )
    user_id: str = Field(
        sa_column=Column("userId", String, nullable=False)
    )
    title: str = Field(
        sa_column=Column("title", String, nullable=False)
    )
    description: Optional[str] = Field(
        default=None,
        sa_column=Column("description", String)
    )
    completed: bool = Field(
        default=False,
        sa_column=Column("completed", Boolean, nullable=False, default=False)
    )
    priority: Optional[PriorityEnum] = Field(
        default=PriorityEnum.medium,
        sa_column=Column("priority", String)
    )
    # Using a custom field for tags to handle the array properly
    tags: Optional[str] = Field(  # Store as JSON string
        default=None,
        sa_column=Column("tags", String)  # Changed from Text to String
    )
    due_date: Optional[datetime] = Field(
        default=None,
        sa_column=Column("dueDate", DateTime)
    )
    recurring_interval: Optional[str] = Field(  # Changed to match the original schema
        default=None,
        sa_column=Column("recurringInterval", String)
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column("createdAt", DateTime, nullable=False)
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column("updatedAt", DateTime, nullable=False)
    )


# Conversation Model for AI Chat History
class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True,
        sa_column=Column("id", String, primary_key=True)
    )
    user_id: str = Field(
        sa_column=Column("userId", String, nullable=False)
    )
    title: str = Field(
        sa_column=Column("title", String, nullable=False)
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column("createdAt", DateTime, nullable=False)
    )


# Message Role Enum
class MessageRoleEnum(str, Enum):
    user = "user"
    assistant = "assistant"


# Message Model for AI Chat History
class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        primary_key=True,
        sa_column=Column("id", String, primary_key=True)
    )
    conversation_id: str = Field(
        sa_column=Column("conversationId", String, nullable=False)
    )
    role: MessageRoleEnum = Field(
        sa_column=Column("role", String, nullable=False)
    )
    content: str = Field(
        sa_column=Column("content", String, nullable=False)
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column("createdAt", DateTime, nullable=False)
    )