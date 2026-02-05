#!/usr/bin/env python3
"""
Self-Verification Script for Backend API
Tests the health endpoint and chat functionality to verify the backend works correctly.
"""

import requests
import json
import sys
import time

BASE_URL = "http://127.0.0.1:8000"

def test_health():
    """Test 1: Ping /health endpoint"""
    print("🧪 Testing Health Endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Health check passed: {data}")
            return True
        else:
            print(f"❌ Health check failed with status {response.status_code}: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Health check failed with error: {e}")
        return False

def test_add_task():
    """Test 2: Send a POST to /api/chat with add task request"""
    print("\n🧪 Testing Add Task Functionality...")
    try:
        payload = {
            "message": "Add a task to buy milk",
            "user_id": "test_user_123"
        }
        response = requests.post(f"{BASE_URL}/api/chat", json=payload)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Add task successful: {data['response'][:100]}...")
            return True
        else:
            print(f"❌ Add task failed with status {response.status_code}: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Add task failed with error: {e}")
        return False

def test_list_tasks():
    """Test 3: Send a POST to /api/chat with list tasks request"""
    print("\n🧪 Testing List Tasks Functionality...")
    try:
        payload = {
            "message": "List my tasks",
            "user_id": "test_user_123"
        }
        response = requests.post(f"{BASE_URL}/api/chat", json=payload)
        if response.status_code == 200:
            data = response.json()
            print(f"✅ List tasks successful: {data['response'][:100]}...")
            return True
        else:
            print(f"❌ List tasks failed with status {response.status_code}: {response.text}")
            return False
    except Exception as e:
        print(f"❌ List tasks failed with error: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Backend Self-Verification Tests...\n")

    # Wait a moment for the server to be ready if it's just starting up
    time.sleep(1)

    results = []

    # Run all tests
    results.append(("Health Check", test_health()))
    results.append(("Add Task", test_add_task()))
    results.append(("List Tasks", test_list_tasks()))

    # Print summary
    print("\n" + "="*50)
    print("📊 TEST RESULTS SUMMARY:")
    print("="*50)

    passed = 0
    total = len(results)

    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<20} {status}")
        if result:
            passed += 1

    print("-"*50)
    print(f"TOTAL: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 ALL TESTS PASSED! Backend is working correctly.")
        print("✅ The AI assistant functionality is verified and operational.")
        return 0
    else:
        print(f"\n💥 {total - passed} test(s) failed. Backend needs attention.")
        return 1

if __name__ == "__main__":
    sys.exit(main())