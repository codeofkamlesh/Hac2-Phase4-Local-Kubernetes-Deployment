"""
MCP Tools for Better Auth Integration
These tools handle task operations for the AI assistant
"""

from sqlmodel import Session, select
from typing import Dict, Any, Optional
from datetime import datetime
import uuid
from dateutil import parser  # for smart date parsing
from models import Task, User, Conversation, Message, PriorityEnum, MessageRoleEnum


def resolve_task_id(session: Session, user_id: str, identifier: str | int) -> int | None:
    """
    Resolve a task identifier (either ID or title) to a database task ID.

    Args:
        session: Database session
        user_id: User ID to scope the search
        identifier: Either a task ID (int) or title (str)

    Returns:
        Database task ID if found, None otherwise
    """
    # Try converting to int (Direct ID)
    try:
        return int(identifier)
    except ValueError:
        # It's a title, look it up
        statement = select(Task).where(Task.title == str(identifier), Task.user_id == user_id)
        task = session.exec(statement).first()
        return task.id if task else None


def add_task(session: Session, title: str, description: Optional[str] = None, priority: str = "medium", due_date: Optional[str] = None, dueDate: Optional[str] = None, tags: Optional[str] = None, recurring: Optional[str] = None, completed: bool = False, user_id: str = "") -> Dict[str, Any]:
    """
    Add a new task to the database

    Args:
        session: Database session
        title: Task title
        description: Optional task description
        priority: Task priority ('high', 'medium', 'low')
        due_date: Optional due date string to parse (alternative param name)
        dueDate: Optional due date string to parse (alternative param name)
        tags: Optional tags for the task
        recurring: Optional recurring interval pattern
        completed: Whether the task is initially completed
        user_id: User ID to associate with the task

    Returns:
        Dictionary with success status and task info
    """
    print(f"🛠️ Executing Tool: add_task with Params: {{'title': '{title}', 'description': '{description}', 'priority': '{priority}', 'due_date': '{due_date}', 'dueDate': '{dueDate}', 'tags': '{tags}', 'recurring': '{recurring}', 'completed': {completed}, 'user_id': '{user_id}'}}")
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

        # Use whichever due date parameter is provided (dueDate takes precedence over due_date)
        effective_due_date = dueDate if dueDate is not None else due_date

        # Parse due_date if provided
        parsed_due_date = None
        if effective_due_date:
            try:
                parsed_due_date = parser.parse(effective_due_date)
            except (ValueError, TypeError):
                print(f"⚠️ Warning: Could not parse due date '{effective_due_date}', using None")
                parsed_due_date = None

        # Normalize Recurrence (map AI variations to proper values)
        recurrence_val = recurring
        if recurrence_val:
            # Normalize common AI variations
            recurrence_val = recurrence_val.lower()
            # Map common variations to standard values
            if recurrence_val in ['daily', 'every day', 'each day']:
                recurrence_val = 'daily'
            elif recurrence_val in ['weekly', 'every week', 'each week']:
                recurrence_val = 'weekly'
            elif recurrence_val in ['monthly', 'every month', 'each month']:
                recurrence_val = 'monthly'
            elif recurrence_val in ['yearly', 'annually', 'every year']:
                recurrence_val = 'yearly'

        # Set recurring flag based on whether there's a recurrence pattern
        recurring_flag = bool(recurrence_val)

        # Create new task with all attributes
        new_task = Task(
            user_id=user_id,  # Use the provided user_id
            title=title,
            description=description,
            completed=completed,
            priority=priority_enum,
            due_date=parsed_due_date,  # Use parsed date
            tags=tags,
            recurring=recurring_flag,  # Set boolean flag based on recurrence value
            recurrence_pattern=recurrence_val,  # Use normalized recurrence value
            recurring_interval=None,  # Clear the old field
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        session.add(new_task)
        session.commit()
        session.refresh(new_task)

        print("✅ Tool Execution Successful")
        return {
            "success": True,
            "message": f"Task '{title}' added successfully with ID {new_task.id}",
            "task_id": new_task.id,
            "task": {
                "id": new_task.id,
                "title": new_task.title,
                "description": new_task.description,
                "completed": new_task.completed,
                "priority": new_task.priority.value if hasattr(new_task.priority, 'value') else new_task.priority,
                "due_date": new_task.due_date.isoformat() if new_task.due_date else None,
                "tags": new_task.tags,
                "recurring": new_task.recurring,
                "recurrence_pattern": new_task.recurrence_pattern
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
        task_id: ID or title of the task to complete
        user_id: User ID to verify task ownership

    Returns:
        Dictionary with success status and task info
    """
    print(f"🛠️ Executing Tool: complete_task with Params: {{'task_id': '{task_id}', 'user_id': '{user_id}'}}")
    try:
        # Use resolve_task_id to handle both IDs and titles
        db_task_id = resolve_task_id(session, user_id, task_id)

        if db_task_id is None:
            print(f"❌ Tool Failed: Task '{task_id}' not found or does not belong to user {user_id}")
            return {
                "success": False,
                "message": f"Task '{task_id}' not found"
            }

        # Find the task using the resolved ID
        query = select(Task).where(Task.id == db_task_id)

        # If user_id is provided, ensure the task belongs to the user
        if user_id:
            query = query.where(Task.user_id == user_id)

        task = session.exec(query).first()

        if not task:
            print(f"❌ Tool Failed: Task with ID {db_task_id} not found or does not belong to user {user_id}")
            return {
                "success": False,
                "message": f"Task with ID {db_task_id} not found"
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
        task_id: ID or title of the task to delete
        user_id: User ID to verify task ownership

    Returns:
        Dictionary with success status
    """
    print(f"🛠️ Executing Tool: delete_task with Params: {{'task_id': '{task_id}', 'user_id': '{user_id}'}}")
    try:
        # Use resolve_task_id to handle both IDs and titles
        db_task_id = resolve_task_id(session, user_id, task_id)

        if db_task_id is None:
            print(f"❌ Tool Failed: Task '{task_id}' not found or does not belong to user {user_id}")
            return {
                "success": False,
                "message": f"Task '{task_id}' not found"
            }

        # Find the task using the resolved ID
        query = select(Task).where(Task.id == db_task_id)

        # If user_id is provided, ensure the task belongs to the user
        if user_id:
            query = query.where(Task.user_id == user_id)

        task = session.exec(query).first()

        if not task:
            print(f"❌ Tool Failed: Task with ID {db_task_id} not found or does not belong to user {user_id}")
            return {
                "success": False,
                "message": f"Task with ID {db_task_id} not found"
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
        task_id: ID or title of the task to update
        updates: Dictionary of fields to update
        user_id: User ID to verify task ownership

    Returns:
        Dictionary with success status and updated task info
    """
    print(f"🛠️ Executing Tool: update_task with Params: {{'task_id': '{task_id}', 'updates': {updates}, 'user_id': '{user_id}'}}")
    try:
        # Step A: Resolve the task ID (handles both IDs and titles)
        db_task_id = resolve_task_id(session, user_id, task_id)

        # Step B: If db_task_id is None, return "Task not found."
        if db_task_id is None:
            print(f"❌ Tool Failed: Task '{task_id}' not found or does not belong to user {user_id}")
            return {
                "success": False,
                "message": f"Task '{task_id}' not found"
            }

        # Find the task using the resolved ID
        query = select(Task).where(Task.id == db_task_id)

        # If user_id is provided, ensure the task belongs to the user
        if user_id:
            query = query.where(Task.user_id == user_id)

        task = session.exec(query).first()

        if not task:
            print(f"❌ Tool Failed: Task with ID {db_task_id} not found or does not belong to user {user_id}")
            return {
                "success": False,
                "message": f"Task with ID {db_task_id} not found"
            }

        # Step C (Date Parsing): Check for dueDate or due_date in updates
        if "dueDate" in updates:
            try:
                updates["due_date"] = parser.parse(updates["dueDate"])
                del updates["dueDate"]  # Remove the old key
            except (ValueError, TypeError):
                print(f"⚠️ Warning: Could not parse due date '{updates['dueDate']}', keeping original value")
        elif "due_date" in updates:
            try:
                updates["due_date"] = parser.parse(updates["due_date"])
            except (ValueError, TypeError):
                print(f"⚠️ Warning: Could not parse due date '{updates['due_date']}', keeping original value")

        # Step D (Mapping): Fix recurrence logic to map to correct columns
        # Normalize Parameters (Map AI guesses to the CORRECT columns)
        # AI often sends these keys that should map to the recurrencePattern column:
        recurrence_keys = ['recurrance_pattern', 'recurring_pattern', 'recurring_interval', 'repeat', 'frequency', 'pattern', 'recurringInterval', 'recurring_interval']

        new_pattern = None
        for key in recurrence_keys:
            if key in updates:
                new_pattern = updates.pop(key)
                break

        # If a pattern was found, Apply the FIX:
        if new_pattern:
            # A. Set the correct text column
            updates['recurrence_pattern'] = new_pattern
            # B. CRITICAL: Set the boolean flag to True
            updates['recurring'] = True
            # C. Clear the incorrect column (optional cleanup)
            updates['recurring_interval'] = None

        # Map 'tag' to 'tags'
        if 'tag' in updates:
            updates['tags'] = updates.pop('tag')

        # Step E: Apply updates
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
            # Use the parsed date
            task.due_date = updates["due_date"]
        if "recurring" in updates:
            # Ensure the value is properly converted to boolean
            val = updates["recurring"]
            if isinstance(val, str):
                task.recurring = val.lower() in ['true', '1', 'yes', 'on']
            else:
                task.recurring = bool(val)
        if "recurrence_pattern" in updates:
            task.recurrence_pattern = updates["recurrence_pattern"]
        if "recurring_interval" in updates:
            task.recurring_interval = updates["recurring_interval"]
        if "tags" in updates:
            task.tags = updates["tags"]

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
                "priority": task.priority.value if hasattr(task.priority, 'value') else task.priority,
                "due_date": task.due_date.isoformat() if task.due_date else None,
                "recurring": task.recurring,
                "recurrence_pattern": task.recurrence_pattern
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