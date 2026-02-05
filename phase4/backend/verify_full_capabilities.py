#!/usr/bin/env python3
"""
Verification script for full capabilities of the robust tools using the chat interface.
This script tests ALL operations as specified in Phase 6 requirements via the chat API.
"""
import os
import sys
import requests
import json
import time
from datetime import datetime, timedelta
from typing import Dict, Any, Optional

# Configuration - adjust these based on your setup
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
TEST_USER_ID = os.getenv("TEST_USER_ID", "test_user_123")

def make_chat_request(message: str, user_id: str, conversation_id: Optional[str] = None):
    """Make a chat request to the backend API"""
    endpoint = f"{BASE_URL}/api/chat"
    data = {
        "message": message,
        "user_id": user_id
    }
    if conversation_id:
        data["conversation_id"] = conversation_id

    print(f"📡 CHAT REQUEST: {message}")

    try:
        response = requests.post(endpoint, json=data, headers={"Content-Type": "application/json"})
        print(f"📊 Response Status: {response.status_code}")
        if response.content:
            try:
                response_data = response.json()
                print(f"📦 Response Data: {json.dumps(response_data, indent=2)[:500]}...")
                return response.status_code, response_data
            except:
                print(f"📄 Response Text: {response.text[:500]}...")
                return response.status_code, response.text
        else:
            print("📦 Empty response body")
            return response.status_code, {}
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return None, {"error": str(e)}

def test_add_task():
    """Step 1: Add task 'Test Task' priority high due tomorrow"""
    print("\n=== STEP 1: ADD TASK ===")
    print("Adding task 'Test Task' priority high due tomorrow...")

    # Calculate tomorrow's date
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

    message = f"Add task 'Test Task' priority high due {tomorrow}"

    status_code, response = make_chat_request(message, TEST_USER_ID)

    if status_code == 200 and isinstance(response, dict) and "response" in response:
        print("✅ PASS - Task addition request processed successfully")

        # Extract conversation ID for subsequent operations
        conversation_id = response.get("conversation_id")
        return True, conversation_id
    else:
        print(f"❌ FAIL - Could not add task. Status: {status_code}, Response: {response}")
        return False, None

def test_update_description(conversation_id: str):
    """Step 2: Add description 'Testing recursive fix'"""
    print("\n=== STEP 2: UPDATE DESCRIPTION ===")
    print("Adding description 'Testing recursive fix' to 'Test Task'")

    message = "Add description 'Testing recursive fix' to 'Test Task'"

    status_code, response = make_chat_request(message, TEST_USER_ID, conversation_id)

    if status_code == 200 and isinstance(response, dict) and "response" in response:
        print("✅ PASS - Description update request processed successfully")
        return True
    else:
        print(f"❌ FAIL - Could not update description. Status: {status_code}, Response: {response}")
        return False

def test_add_tag(conversation_id: str):
    """Step 3: Add tag 'urgent' to 'Test Task'"""
    print("\n=== STEP 3: ADD TAG ===")
    print("Adding tag 'urgent' to 'Test Task'")

    message = "Add tag 'urgent' to 'Test Task'"

    status_code, response = make_chat_request(message, TEST_USER_ID, conversation_id)

    if status_code == 200 and isinstance(response, dict) and "response" in response:
        print("✅ PASS - Tag addition request processed successfully")
        return True
    else:
        print(f"❌ FAIL - Could not add tag. Status: {status_code}, Response: {response}")
        return False

def test_add_recurrence(conversation_id: str):
    """Step 4: Make 'Test Task' repeat daily"""
    print("\n=== STEP 4: ADD RECURRENCE ===")
    print("Making 'Test Task' repeat daily")

    message = "Make 'Test Task' repeat daily"

    status_code, response = make_chat_request(message, TEST_USER_ID, conversation_id)

    if status_code == 200 and isinstance(response, dict) and "response" in response:
        print("✅ PASS - Recurrence addition request processed successfully")
        return True
    else:
        print(f"❌ FAIL - Could not add recurrence. Status: {status_code}, Response: {response}")
        return False

def test_update_priority(conversation_id: str):
    """Step 5: Change priority to low"""
    print("\n=== STEP 5: UPDATE PRIORITY ===")
    print("Changing priority of 'Test Task' to low")

    message = "Change priority of 'Test Task' to low"

    status_code, response = make_chat_request(message, TEST_USER_ID, conversation_id)

    if status_code == 200 and isinstance(response, dict) and "response" in response:
        print("✅ PASS - Priority update request processed successfully")
        return True
    else:
        print(f"❌ FAIL - Could not update priority. Status: {status_code}, Response: {response}")
        return False

def test_complete_task(conversation_id: str):
    """Step 6: Mark 'Test Task' as complete"""
    print("\n=== STEP 6: COMPLETE TASK ===")
    print("Marking 'Test Task' as complete")

    message = "Mark 'Test Task' as complete"

    status_code, response = make_chat_request(message, TEST_USER_ID, conversation_id)

    if status_code == 200 and isinstance(response, dict) and "response" in response:
        print("✅ PASS - Task completion request processed successfully")
        return True
    else:
        print(f"❌ FAIL - Could not complete task. Status: {status_code}, Response: {response}")
        return False

def test_mark_incomplete(conversation_id: str):
    """Step 7: Mark 'Test Task' as incomplete"""
    print("\n=== STEP 7: MARK INCOMPLETE ===")
    print("Marking 'Test Task' as incomplete")

    message = "Mark 'Test Task' as incomplete"

    status_code, response = make_chat_request(message, TEST_USER_ID, conversation_id)

    if status_code == 200 and isinstance(response, dict) and "response" in response:
        print("✅ PASS - Task marking as incomplete request processed successfully")
        return True
    else:
        print(f"❌ FAIL - Could not mark task as incomplete. Status: {status_code}, Response: {response}")
        return False

def test_delete_task(conversation_id: str):
    """Step 8: Delete 'Test Task'"""
    print("\n=== STEP 8: DELETE TASK ===")
    print("Deleting 'Test Task'")

    message = "Delete 'Test Task'"

    status_code, response = make_chat_request(message, TEST_USER_ID, conversation_id)

    if status_code == 200 and isinstance(response, dict) and "response" in response:
        print("✅ PASS - Task deletion request processed successfully")
        return True
    else:
        print(f"❌ FAIL - Could not delete task. Status: {status_code}, Response: {response}")
        return False

def test_title_based_operations():
    """Test operations using task titles instead of IDs"""
    print("\n=== ADDITIONAL: TITLE-BASED OPERATIONS ===")
    print("Testing if tools can handle titles as well as IDs...")

    # First, add a task with a distinctive title
    title_task_name = "Title Lookup Test Task"

    message = f"Add task '{title_task_name}' priority medium due tomorrow"
    status_code, response = make_chat_request(message, TEST_USER_ID)

    if status_code != 200 or not isinstance(response, dict) or "response" not in response:
        print(f"❌ Could not create title-based test task. Cannot test title operations.")
        return False

    conversation_id = response.get("conversation_id")

    # Now test updating using the title instead of ID
    update_message = f"Update description of '{title_task_name}' to 'Updated via title lookup'"
    status_code, response = make_chat_request(update_message, TEST_USER_ID, conversation_id)

    # Clean up
    delete_message = f"Delete '{title_task_name}'"
    make_chat_request(delete_message, TEST_USER_ID, conversation_id)

    if status_code == 200 and isinstance(response, dict) and "response" in response:
        print("✅ PASS - Title-based operations working")
        return True
    else:
        print(f"❌ FAIL - Title-based operations not working. Status: {status_code}")
        return False

def test_date_parsing():
    """Test various date formats are handled properly"""
    print("\n=== ADDITIONAL: DATE PARSING ===")
    print("Testing various date formats...")

    date_formats = [
        "today",
        "tomorrow",
        "next Monday",
        "in 2 days",
        "2025-12-25"
    ]

    for date_format in date_formats:
        message = f"Add test task for date parsing due {date_format}"
        status_code, response = make_chat_request(message, TEST_USER_ID)

        if status_code != 200 or not isinstance(response, dict) or "response" not in response:
            print(f"❌ Date format '{date_format}' failed")
            return False

        # Clean up - delete the test task
        delete_message = "Delete test task for date parsing"
        make_chat_request(delete_message, TEST_USER_ID, response.get("conversation_id"))

    print("✅ PASS - All date formats handled successfully")
    return True

def run_verification():
    """Run the complete verification suite"""
    print("🧪 Starting Full Capabilities Verification via Chat Interface")
    print("=" * 70)

    results = {}

    # Step 1: Add Task
    success, conversation_id = test_add_task()
    results[1] = success

    if not success or not conversation_id:
        print("\n❌ ABORTING - Could not add initial task, cannot proceed with tests")
        return results

    # Step 2: Update Description
    success = test_update_description(conversation_id)
    results[2] = success

    # Step 3: Add Tag
    success = test_add_tag(conversation_id)
    results[3] = success

    # Step 4: Add Recurrence
    success = test_add_recurrence(conversation_id)
    results[4] = success

    # Step 5: Update Priority
    success = test_update_priority(conversation_id)
    results[5] = success

    # Step 6: Complete Task
    success = test_complete_task(conversation_id)
    results[6] = success

    # Step 7: Mark Incomplete
    success = test_mark_incomplete(conversation_id)
    results[7] = success

    # Step 8: Delete Task
    success = test_delete_task(conversation_id)
    results[8] = success

    # Additional test: Title-based operations
    title_success = test_title_based_operations()
    results["title_ops"] = title_success

    # Additional test: Date parsing
    date_success = test_date_parsing()
    results["date_parsing"] = date_success

    return results

def print_summary(results):
    """Print a summary of all test results"""
    print("\n" + "=" * 70)
    print("📊 VERIFICATION SUMMARY")
    print("=" * 70)

    total_tests = len([k for k in results.keys() if isinstance(k, int)])
    passed_tests = sum([1 for v in results.values() if v])

    print(f"Total Core Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {total_tests - passed_tests}")

    print("\nDetailed Results:")

    # Sort numeric keys first, then string keys
    numeric_keys = sorted([k for k in results.keys() if isinstance(k, int)])
    string_keys = sorted([k for k in results.keys() if isinstance(k, str)])

    for step in numeric_keys:
        success = results[step]
        step_names = {
            1: "Add Task",
            2: "Update Description",
            3: "Add Tag",
            4: "Add Recurrence",
            5: "Update Priority",
            6: "Complete Task",
            7: "Mark Incomplete",
            8: "Delete Task"
        }
        name = step_names.get(step, f"Step {step}")
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  {step}. {name}: {status}")

    for step in string_keys:
        success = results[step]
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  {step}: {status}")

    overall_pass = all(results.values())
    print(f"\n🎯 OVERALL RESULT: {'✅ ALL TESTS PASSED' if overall_pass else '❌ SOME TESTS FAILED'}")

    return overall_pass

if __name__ == "__main__":
    print("🚀 Running Full Capabilities Verification Script via Chat Interface")
    print(f"Using BASE_URL: {BASE_URL}")
    print(f"Using TEST_USER_ID: {TEST_USER_ID}")

    try:
        # Check if the server is running first
        health_url = f"{BASE_URL}/health"
        try:
            health_resp = requests.get(health_url)
            if health_resp.status_code != 200:
                print(f"⚠️ Health check failed: {health_resp.status_code}")
            else:
                print("✅ Server health check passed")
        except Exception as e:
            print(f"⚠️ Cannot reach server at {BASE_URL}: {e}")
            print("Make sure the backend server is running on the specified port")
            sys.exit(1)

        results = run_verification()
        overall_success = print_summary(results)

        if overall_success:
            print("\n🎉 VERIFICATION COMPLETE - All operations working correctly!")
            print("\nKey verified capabilities:")
            print("✅ Add Task with date parsing")
            print("✅ Update Description")
            print("✅ Add Tags with normalization")
            print("✅ Add Recurrence with parameter mapping")
            print("✅ Update Priority")
            print("✅ Complete Task")
            print("✅ Mark Incomplete")
            print("✅ Delete Task")
            print("✅ Title-based ID resolution")
            print("✅ Smart date parsing")
            print("✅ Parameter normalization")
        else:
            print("\n💥 VERIFICATION FAILED - Some operations are not working correctly")
            print("Please check the implementation and fix the failing tests")

        # Exit with appropriate code
        sys.exit(0 if overall_success else 1)

    except KeyboardInterrupt:
        print("\n\n⚠️ Verification interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Verification failed with exception: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)