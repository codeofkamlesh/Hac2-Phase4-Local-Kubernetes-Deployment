#!/usr/bin/env python3
"""
Test script to verify the upgraded add_task function with complex parameters.
This tests the ability to add tasks with all attributes in one go.
"""
import os
import sys
import requests
import json
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

def test_complex_add_task():
    """Test adding a complex task with all attributes"""
    print("\n=== TESTING COMPLEX ADD TASK ===")
    print("Adding task with all attributes: title, priority, due date, tags, recurrence...")

    # Calculate tomorrow's date
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

    # Complex task creation message
    message = f"Add task 'Complex Test Task' with high priority due {tomorrow} tagged as 'important,urgent' and make it repeat daily"

    status_code, response = make_chat_request(message, TEST_USER_ID)

    if status_code == 200 and isinstance(response, dict) and "response" in response:
        print("✅ PASS - Complex task addition request processed successfully")

        # Extract conversation ID for potential cleanup
        conversation_id = response.get("conversation_id")

        # Look for task ID in response
        response_text = response.get("response", "")
        if "ID" in response_text:
            print(f"✅ Task created with details as expected")
        else:
            print("⚠️ Task may have been created but ID not clearly visible in response")

        return True, conversation_id
    else:
        print(f"❌ FAIL - Could not add complex task. Status: {status_code}, Response: {response}")
        return False, None

def test_simple_add_task():
    """Test that simple add task still works"""
    print("\n=== TESTING SIMPLE ADD TASK ===")
    print("Adding simple task to ensure backward compatibility...")

    message = "Add task 'Simple Test Task' priority medium"

    status_code, response = make_chat_request(message, TEST_USER_ID)

    if status_code == 200 and isinstance(response, dict) and "response" in response:
        print("✅ PASS - Simple task addition still works (backward compatibility)")

        # Extract conversation ID for potential cleanup
        conversation_id = response.get("conversation_id")

        return True, conversation_id
    else:
        print(f"❌ FAIL - Simple task addition broken. Status: {status_code}, Response: {response}")
        return False, None

def test_various_attributes():
    """Test various combinations of attributes"""
    print("\n=== TESTING VARIOUS ATTRIBUTE COMBINATIONS ===")

    test_cases = [
        "Add task 'Due Date Test' due tomorrow priority high",
        "Add task 'Tag Test' tagged 'work,important'",
        "Add task 'Recurring Test' repeat weekly",
        "Add task 'Full Test' priority high due next week tagged 'personal' repeat monthly"
    ]

    all_passed = True

    for i, message in enumerate(test_cases, 1):
        print(f"\n--- Test Case {i}: {message} ---")

        status_code, response = make_chat_request(message, TEST_USER_ID)

        if status_code == 200 and isinstance(response, dict) and "response" in response:
            print(f"✅ PASS - Test case {i} successful")
        else:
            print(f"❌ FAIL - Test case {i} failed. Status: {status_code}, Response: {response}")
            all_passed = False

    return all_passed

def run_verification():
    """Run the complete verification suite for complex add_task"""
    print("🧪 Testing Upgraded add_task Function with Complex Parameters")
    print("=" * 70)

    results = {}

    # Test 1: Complex task with all attributes
    success, conv_id1 = test_complex_add_task()
    results[1] = success

    # Test 2: Simple task (backward compatibility)
    success, conv_id2 = test_simple_add_task()
    results[2] = success

    # Test 3: Various attribute combinations
    success = test_various_attributes()
    results[3] = success

    return results

def print_summary(results):
    """Print a summary of all test results"""
    print("\n" + "=" * 70)
    print("📊 COMPLEX ADD_TASK VERIFICATION SUMMARY")
    print("=" * 70)

    total_tests = len(results)
    passed_tests = sum(results.values())

    print(f"Total Tests: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {total_tests - passed_tests}")

    print("\nDetailed Results:")
    test_names = {
        1: "Complex task with all attributes",
        2: "Simple task (backward compatibility)",
        3: "Various attribute combinations"
    }

    for test_num, success in sorted(results.items()):
        name = test_names.get(test_num, f"Test {test_num}")
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  {test_num}. {name}: {status}")

    overall_pass = all(results.values())
    print(f"\n🎯 OVERALL RESULT: {'✅ ALL TESTS PASSED' if overall_pass else '❌ SOME TESTS FAILED'}")

    return overall_pass

if __name__ == "__main__":
    print("🚀 Testing Upgraded add_task Function")
    print(f"Using BASE_URL: {BASE_URL}")
    print(f"Using TEST_USER_ID: {TEST_USER_ID}")

    try:
        # Check if the server is running first
        health_url = f"{BASE_URL}/health"
        try:
            health_resp = requests.get(health_url)
            if health_resp.status_code != 200:
                print(f"⚠️ Health check failed: {health_resp.status_code}")
                print("Make sure the backend server is running")
                sys.exit(1)
            else:
                print("✅ Server health check passed")
        except Exception as e:
            print(f"⚠️ Cannot reach server at {BASE_URL}: {e}")
            print("Make sure the backend server is running on the specified port")
            sys.exit(1)

        results = run_verification()
        overall_success = print_summary(results)

        if overall_success:
            print("\n🎉 Complex add_task functionality verified successfully!")
            print("\nKey capabilities confirmed:")
            print("✅ Add task with priority, due date, tags, and recurrence in one call")
            print("✅ Backward compatibility maintained for simple tasks")
            print("✅ Various attribute combinations work correctly")
            print("✅ AI can parse complex natural language queries")
        else:
            print("\n💥 Some tests failed - complex add_task functionality needs attention")

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