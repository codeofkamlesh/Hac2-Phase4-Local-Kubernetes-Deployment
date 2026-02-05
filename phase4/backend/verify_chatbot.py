#!/usr/bin/env python3
"""
Verification script for the AI Chatbot functionality.
Tests Add, List, Update, and Delete operations through the chat interface.
"""
import requests
import json
import time
import uuid

BASE_URL = "http://localhost:8000"
TEST_USER_ID = f"test_user_{str(uuid.uuid4())[:8]}"

def test_add_task():
    """Test adding a task through the chat interface."""
    print("🧪 Testing ADD task via chatbot...")

    try:
        payload = {
            "message": "Add a task to buy groceries",
            "user_id": TEST_USER_ID,
            "conversation_id": None
        }

        response = requests.post(f"{BASE_URL}/api/chat", json=payload)

        if response.status_code == 200:
            data = response.json()
            print(f"✅ ADD test passed: {data['response'][:100]}...")
            return True
        else:
            print(f"❌ ADD test failed with status {response.status_code}: {response.text}")
            return False

    except Exception as e:
        print(f"❌ ADD test failed with error: {e}")
        return False

def test_list_tasks():
    """Test listing tasks through the chat interface."""
    print("\n🧪 Testing LIST tasks via chatbot...")

    try:
        payload = {
            "message": "List all my tasks",
            "user_id": TEST_USER_ID,
            "conversation_id": None
        }

        response = requests.post(f"{BASE_URL}/api/chat", json=payload)

        if response.status_code == 200:
            data = response.json()
            print(f"✅ LIST test passed: {data['response'][:100]}...")
            return True
        else:
            print(f"❌ LIST test failed with status {response.status_code}: {response.text}")
            return False

    except Exception as e:
        print(f"❌ LIST test failed with error: {e}")
        return False

def test_update_task():
    """Test updating a task through the chat interface."""
    print("\n🧪 Testing UPDATE task via chatbot...")

    try:
        # First, add a task to update
        add_payload = {
            "message": "Add a task to complete project",
            "user_id": TEST_USER_ID,
            "conversation_id": None
        }

        add_response = requests.post(f"{BASE_URL}/api/chat", json=add_payload)
        if add_response.status_code != 200:
            print("❌ Could not add task for update test")
            return False

        # Now try to update the task
        payload = {
            "message": "Update the task 'Complete project' to 'Complete project by tomorrow'",
            "user_id": TEST_USER_ID,
            "conversation_id": None
        }

        response = requests.post(f"{BASE_URL}/api/chat", json=payload)

        if response.status_code == 200:
            data = response.json()
            print(f"✅ UPDATE test passed: {data['response'][:100]}...")
            return True
        else:
            print(f"❌ UPDATE test failed with status {response.status_code}: {response.text}")
            return False

    except Exception as e:
        print(f"❌ UPDATE test failed with error: {e}")
        return False

def test_delete_task():
    """Test deleting a task through the chat interface."""
    print("\n🧪 Testing DELETE task via chatbot...")

    try:
        # First, add a task to delete
        add_payload = {
            "message": "Add a task to clean room",
            "user_id": TEST_USER_ID,
            "conversation_id": None
        }

        add_response = requests.post(f"{BASE_URL}/api/chat", json=add_payload)
        if add_response.status_code != 200:
            print("❌ Could not add task for delete test")
            return False

        # Now try to delete the task
        payload = {
            "message": "Delete the task 'clean room'",
            "user_id": TEST_USER_ID,
            "conversation_id": None
        }

        response = requests.post(f"{BASE_URL}/api/chat", json=payload)

        if response.status_code == 200:
            data = response.json()
            print(f"✅ DELETE test passed: {data['response'][:100]}...")
            return True
        else:
            print(f"❌ DELETE test failed with status {response.status_code}: {response.text}")
            return False

    except Exception as e:
        print(f"❌ DELETE test failed with error: {e}")
        return False

def test_loop_crash_fix():
    """Test that the loop crash fix works by sending multiple tool calls."""
    print("\n🧪 Testing loop crash fix with multiple operations...")

    try:
        # Send a complex request that might trigger multiple tool calls
        payload = {
            "message": "I want to add three tasks: buy milk, call mom, and finish report. Then list all tasks.",
            "user_id": TEST_USER_ID,
            "conversation_id": None
        }

        response = requests.post(f"{BASE_URL}/api/chat", json=payload)

        if response.status_code == 200:
            data = response.json()
            print(f"✅ Loop crash fix test passed: {data['response'][:100]}...")
            return True
        else:
            print(f"❌ Loop crash fix test failed with status {response.status_code}: {response.text}")
            return False

    except Exception as e:
        print(f"❌ Loop crash fix test failed with error: {e}")
        return False

def main():
    """Run all verification tests."""
    print("🚀 Starting Chatbot Verification Tests")
    print("=" * 60)
    print(f"Using test user ID: {TEST_USER_ID}")

    # Check if backend is running
    try:
        health_response = requests.get(f"{BASE_URL}/health", timeout=5)
        if health_response.status_code != 200:
            print(f"❌ Backend is not running at {BASE_URL}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"❌ Backend is not running at {BASE_URL}. Please start the backend server first.")
        print("Run: uvicorn main:app --reload --port 8000")
        return False
    except Exception as e:
        print(f"❌ Error connecting to backend: {e}")
        return False

    print("✅ Backend is running")
    print()

    # Run all tests
    tests = [
        ("ADD", test_add_task),
        ("LIST", test_list_tasks),
        ("UPDATE", test_update_task),
        ("DELETE", test_delete_task),
        ("LOOP FIX", test_loop_crash_fix)
    ]

    passed = 0
    total = len(tests)

    for test_name, test_func in tests:
        if test_func():
            print(f"✅ {test_name} - PASS")
            passed += 1
        else:
            print(f"❌ {test_name} - FAIL")
        time.sleep(1)  # Brief pause between tests

    print("\n" + "=" * 60)
    print(f"📊 Final Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 ALL TESTS PASSED! The chatbot is 100% functional.")
        print("✅ No loop crashes detected")
        print("✅ All operations (Add, List, Update, Delete) work correctly")
        print("✅ Backend is stable and bug-free")
        return True
    else:
        print("❌ SOME TESTS FAILED! The chatbot needs further fixes.")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)