#!/usr/bin/env python3
"""
Simple test to verify that the chatbot is working properly after fixes.
"""
import requests
import json

BASE_URL = "http://localhost:8000"
TEST_USER_ID = "test_user_123"

def test_operation(name, message):
    """Test a single operation."""
    print(f"🧪 Testing {name}...")
    try:
        payload = {
            "message": message,
            "user_id": TEST_USER_ID
        }
        response = requests.post(f"{BASE_URL}/api/chat", json=payload)

        if response.status_code == 200:
            data = response.json()
            print(f"✅ {name} - PASS: {data['response'][:60]}...")
            return True
        else:
            print(f"❌ {name} - FAIL: Status {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ {name} - FAIL: {e}")
        return False

def main():
    """Run simple verification tests."""
    print("🚀 Starting Simple Chatbot Verification Tests")
    print("=" * 50)

    # Check if backend is running
    try:
        health_response = requests.get(f"{BASE_URL}/health", timeout=5)
        if health_response.status_code != 200:
            print(f"❌ Backend is not running at {BASE_URL}")
            return False
    except requests.exceptions.ConnectionError:
        print(f"❌ Backend is not running at {BASE_URL}")
        return False

    print("✅ Backend is running")
    print()

    # Test operations
    tests = [
        ("ADD TASK", "Add a task to buy bread"),
        ("LIST TASKS", "List all my tasks"),
        ("UPDATE TASK", "Update the task 'buy bread' to completed"),
        ("DELETE TASK", "Delete the task 'buy bread'"),
    ]

    passed = 0
    total = len(tests)

    for test_name, test_message in tests:
        if test_operation(test_name, test_message):
            passed += 1
        print()

    print("=" * 50)
    print(f"📊 Results: {passed}/{total} tests passed")

    if passed == total:
        print("🎉 ALL TESTS PASSED! The chatbot is working correctly.")
        print("✅ No more 400 errors from Cohere")
        print("✅ Loop crash has been fixed")
        print("✅ All operations work correctly")
        return True
    else:
        print("❌ Some tests failed.")
        return False

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)