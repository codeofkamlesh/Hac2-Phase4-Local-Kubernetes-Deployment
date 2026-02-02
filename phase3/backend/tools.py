"""
MCP Tools for Better Auth Integration
These tools handle task operations for the AI assistant
"""

from sqlmodel import Session, select
from typing import Dict, Any, Optional
from datetime import datetime
import uuid
from models import Task, User, Conversation, Message, PriorityEnum, MessageRoleEnum


def add_task(session: Session, title: str, description: Optional[str] = None, priority: str = "medium", user_id: str = "") -> Dict[str, Any]:
    """
    Add a new task to the database

    Args:
        session: Database session
        title: Task title
        description: Optional task description
        priority: Task priority ('high', 'medium', 'low')
        user_id: User ID to associate with the task

    Returns:
        Dictionary with success status and task info
    """
    print(f"🛠️ Executing Tool: add_task with Params: {{'title': '{title}', 'description': '{description}', 'priority': '{priority}', 'user_id': '{user_id}'}}")
    try:
        # Validate priority
        if priority not in ["high", "medium", "low"]:
            priority = "medium"

        # Handle enum conversion - convert string to enum if needed
        priority_enum = priority
        if isinstance(priority, str) and hasattr(PriorityEnum, priority.lower()):
            priority_enum = PriorityEnum(priority.lower())
        elif isinstance(priority, str):
            priority_enum = PriorityEnum(priority)
        elif hasattr(priority, 'value'):
            priority_enum = priority  # Already an enum
        else:
            priority_enum = PriorityEnum(priority)

        # Create new task
        new_task = Task(
            user_id=user_id,  # Use the provided user_id
            title=title,
            description=description,
            completed=False,
            priority=priority_enum,
            due_date=None,  # Would be parsed from user request if needed
            recurring_interval=None,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        session.add(new_task)
        session.commit()
        session.refresh(new_task)

        print("✅ Tool Execution Successful")
        return {
            "success": True,
            "message": f"Task '{title}' added successfully",
            "task_id": new_task.id,
            "task": {
                "id": new_task.id,
                "title": new_task.title,
                "description": new_task.description,
                "completed": new_task.completed,
                "priority": new_task.priority.value if hasattr(new_task.priority, 'value') else new_task.priority
            }
        }
    except Exception as e:
        session.rollback()
        print(f"❌ Tool Failed: {str(e)}")
        return {
            "success": False,
            "message": f"Failed to add task: {str(e)}"
        }


def list_tasks(session: Session, status: Optional[str] = None, limit: int = 10, user_id: str = "") -> Dict[str, Any]:
    """
    List tasks with optional filtering

    Args:
        session: Database session
        status: Filter by status ('completed', 'pending', None for all)
        limit: Maximum number of tasks to return
        user_id: User ID to filter tasks by

    Returns:
        Dictionary with success status and task list
    """
    print(f"🛠️ Executing Tool: list_tasks with Params: {{'status': '{status}', 'limit': {limit}, 'user_id': '{user_id}'}}")
    try:
        # Build query
        query = select(Task)

        # Filter by user_id if provided
        if user_id:
            query = query.where(Task.user_id == user_id)

        if status == "completed":
            query = query.where(Task.completed == True)
        elif status == "pending":
            query = query.where(Task.completed == False)

        # Apply limit
        query = query.limit(limit)

        # Execute query
        tasks = session.exec(query).all()

        task_list = []
        for task in tasks:
            task_list.append({
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "priority": task.priority.value if hasattr(task.priority, 'value') else task.priority,
                "due_date": task.due_date.isoformat() if task.due_date else None,
                "created_at": task.created_at.isoformat() if task.created_at else None
            })

        print("✅ Tool Execution Successful")
        return {
            "success": True,
            "message": f"Retrieved {len(task_list)} tasks",
            "tasks": task_list,
            "count": len(task_list)
        }
    except Exception as e:
        print(f"❌ Tool Failed: {str(e)}")
        return {
            "success": False,
            "message": f"Failed to list tasks: {str(e)}"
        }


def complete_task(session: Session, task_id: str, user_id: str = "") -> Dict[str, Any]:
    """
    Mark a task as completed

    Args:
        session: Database session
        task_id: ID of the task to complete
        user_id: User ID to verify task ownership

    Returns:
        Dictionary with success status and task info
    """
    print(f"🛠️ Executing Tool: complete_task with Params: {{'task_id': '{task_id}', 'user_id': '{user_id}'}}")
    try:
        # Find the task
        query = select(Task).where(Task.id == int(task_id))

        # If user_id is provided, ensure the task belongs to the user
        if user_id:
            query = query.where(Task.user_id == user_id)

        task = session.exec(query).first()

        if not task:
            print(f"❌ Tool Failed: Task with ID {task_id} not found or does not belong to user {user_id}")
            return {
                "success": False,
                "message": f"Task with ID {task_id} not found"
            }

        # Update task status
        task.completed = True
        task.updated_at = datetime.utcnow()
        session.add(task)
        session.commit()
        session.refresh(task)

        print("✅ Tool Execution Successful")
        return {
            "success": True,
            "message": f"Task '{task.title}' marked as completed",
            "task": {
                "id": task.id,
                "title": task.title,
                "completed": task.completed
            }
        }
    except Exception as e:
        session.rollback()
        print(f"❌ Tool Failed: {str(e)}")
        return {
            "success": False,
            "message": f"Failed to complete task: {str(e)}"
        }


def delete_task(session: Session, task_id: str, user_id: str = "") -> Dict[str, Any]:
    """
    Delete a task from the database

    Args:
        session: Database session
        task_id: ID of the task to delete
        user_id: User ID to verify task ownership

    Returns:
        Dictionary with success status
    """
    print(f"🛠️ Executing Tool: delete_task with Params: {{'task_id': '{task_id}', 'user_id': '{user_id}'}}")
    try:
        # Find the task
        query = select(Task).where(Task.id == int(task_id))

        # If user_id is provided, ensure the task belongs to the user
        if user_id:
            query = query.where(Task.user_id == user_id)

        task = session.exec(query).first()

        if not task:
            print(f"❌ Tool Failed: Task with ID {task_id} not found or does not belong to user {user_id}")
            return {
                "success": False,
                "message": f"Task with ID {task_id} not found"
            }

        # Delete the task
        session.delete(task)
        session.commit()

        print("✅ Tool Execution Successful")
        return {
            "success": True,
            "message": f"Task '{task.title}' deleted successfully"
        }
    except Exception as e:
        session.rollback()
        print(f"❌ Tool Failed: {str(e)}")
        return {
            "success": False,
            "message": f"Failed to delete task: {str(e)}"
        }


def update_task(session: Session, task_id: str, updates: Dict[str, Any], user_id: str = "") -> Dict[str, Any]:
    """
    Update a task with new information

    Args:
        session: Database session
        task_id: ID of the task to update
        updates: Dictionary of fields to update
        user_id: User ID to verify task ownership

    Returns:
        Dictionary with success status and updated task info
    """
    print(f"🛠️ Executing Tool: update_task with Params: {{'task_id': '{task_id}', 'updates': {updates}, 'user_id': '{user_id}'}}")
    try:
        # Find the task
        query = select(Task).where(Task.id == int(task_id))

        # If user_id is provided, ensure the task belongs to the user
        if user_id:
            query = query.where(Task.user_id == user_id)

        task = session.exec(query).first()

        if not task:
            print(f"❌ Tool Failed: Task with ID {task_id} not found or does not belong to user {user_id}")
            return {
                "success": False,
                "message": f"Task with ID {task_id} not found"
            }

        # Apply updates
        if "title" in updates and updates["title"]:
            task.title = updates["title"]
        if "description" in updates:
            task.description = updates["description"]
        if "completed" in updates:
            task.completed = updates["completed"]
        if "priority" in updates and updates["priority"] in ["high", "medium", "low"]:
            # Handle enum conversion - convert string to enum if needed
            priority_value = updates["priority"]
            if isinstance(priority_value, str) and hasattr(PriorityEnum, priority_value.lower()):
                task.priority = PriorityEnum(priority_value.lower())
            elif isinstance(priority_value, str):
                task.priority = PriorityEnum(priority_value)
            elif hasattr(priority_value, 'value'):
                task.priority = priority_value  # Already an enum
            else:
                task.priority = PriorityEnum(priority_value)
        if "due_date" in updates:
            # This would require parsing the date string appropriately
            task.due_date = updates["due_date"]

        task.updated_at = datetime.utcnow()
        session.add(task)
        session.commit()
        session.refresh(task)

        print("✅ Tool Execution Successful")
        return {
            "success": True,
            "message": f"Task '{task.title}' updated successfully",
            "task": {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "priority": task.priority.value if hasattr(task.priority, 'value') else task.priority
            }
        }
    except Exception as e:
        session.rollback()
        print(f"❌ Tool Failed: {str(e)}")
        return {
            "success": False,
            "message": f"Failed to update task: {str(e)}"
        }


def get_conversation_history(conversation_id: str, session: Session) -> list:
    """
    Retrieve conversation history for a specific conversation

    Args:
        conversation_id: ID of the conversation
        session: Database session

    Returns:
        List of messages in the conversation
    """
    try:
        messages = session.exec(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at)
        ).all()

        message_list = []
        for msg in messages:
            message_list.append({
                "role": msg.role,
                "content": msg.content,
                "timestamp": msg.created_at.isoformat()
            })

        return message_list
    except Exception as e:
        print(f"Error retrieving conversation history: {str(e)}")
        return []


def add_message_to_conversation(conversation_id: str, role: str, content: str, session: Session) -> bool:
    """
    Add a message to a conversation

    Args:
        conversation_id: ID of the conversation
        role: Role of the message ('user' or 'assistant')
        content: Content of the message
        session: Database session

    Returns:
        Boolean indicating success
    """
    try:
        # Validate role
        if role not in ["user", "assistant"]:
            role = "assistant"

        role_enum = MessageRoleEnum.assistant if role == "assistant" else MessageRoleEnum.user

        # Create new message
        new_message = Message(
            id=str(uuid.uuid4()),
            conversation_id=conversation_id,
            role=role_enum,
            content=content,
            created_at=datetime.utcnow()
        )

        session.add(new_message)
        session.commit()

        return True
    except Exception as e:
        session.rollback()
        print(f"Error adding message to conversation: {str(e)}")
        return False