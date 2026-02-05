import os
from typing import Dict, Any, List
from cohere import Client as CohereClient
from .tools import (
    add_task,
    list_tasks,
    complete_task,
    delete_task,
    update_task
)
from sqlmodel import Session


def get_cohere_client():
    """
    Initialize and return Cohere client
    """
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        raise ValueError("COHERE_API_KEY environment variable is not set")
    return CohereClient(api_key=api_key)


def run_agent(message: str, history: List[Dict[str, str]], user_id: str, session: Session) -> str:
    """
    Main agent function that processes user messages using Cohere and executes tools

    Args:
        message: User's input message
        history: Chat history for context
        user_id: ID of the authenticated user
        session: Database session for tool operations

    Returns:
        AI-generated response string
    """
    try:
        cohere_client = get_cohere_client()

        # Prepare chat history for Cohere
        formatted_history = []
        for msg in history:
            formatted_history.append({
                "role": msg["role"],
                "message": msg["content"]
            })

        # Define tools that Cohere can use
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

        # Call Cohere with tools
        response = cohere_client.chat(
            message=message,
            chat_history=formatted_history,
            tools=tools,
            model="command-r-plus"  # Using a model with strong tool use capabilities
        )

        # Process the response
        ai_response = ""

        if hasattr(response, 'tool_calls') and response.tool_calls:
            # Process tool calls
            for tool_call in response.tool_calls:
                tool_name = tool_call.name
                tool_parameters = tool_call.parameters

                # Execute the appropriate tool
                if tool_name == "add_task":
                    result = add_task(session, **tool_parameters)
                elif tool_name == "list_tasks":
                    result = list_tasks(session, **tool_parameters)
                elif tool_name == "complete_task":
                    result = complete_task(session, **tool_parameters)
                elif tool_name == "delete_task":
                    result = delete_task(session, **tool_parameters)
                elif tool_name == "update_task":
                    result = update_task(session, **tool_parameters)
                else:
                    result = {"success": False, "message": f"Unknown tool: {tool_name}"}

                # Add tool result to chat for follow-up
                ai_response += f"\nTool result: {result.get('message', str(result))}"
        else:
            # If no tool was called, use the text response
            if hasattr(response, 'text'):
                ai_response = response.text
            else:
                ai_response = "I processed your request, but I don't have a specific response to return."

        return ai_response

    except Exception as e:
        # Return error message if something goes wrong
        return f"Sorry, I encountered an error processing your request: {str(e)}"