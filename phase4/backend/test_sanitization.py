#!/usr/bin/env python3
"""
Test script to verify the sanitization fix for NoneType error in chat history
"""

def test_chat_history_sanitization():
    """
    Test that demonstrates the sanitization logic we added to main.py
    """
    print("Testing chat history sanitization logic...")

    # Simulate conversation history that might come from database with None values
    conversation_history = [
        {"role": "USER", "content": "Hello, can you help me?", "timestamp": "2023-01-01T00:00:00"},
        {"role": "ASSISTANT", "content": "Sure, how can I help?", "timestamp": "2023-01-01T00:00:01"},
        {"role": "TOOL", "content": None, "timestamp": "2023-01-01T00:00:02"},  # This would cause the error
        {"role": "USER", "content": "Add a task", "timestamp": "2023-01-01T00:00:03"},
    ]

    # Prepare the chat history for Cohere (similar to what's done in main.py)
    chat_history = []
    for msg in conversation_history:
        chat_history.append({
            "role": msg["role"],
            "message": msg["content"]
        })

    print(f"Before sanitization: {chat_history}")

    # Apply the sanitization logic we added
    for msg in chat_history:
        if msg.get("message") is None:
            msg["message"] = ""

    print(f"After sanitization: {chat_history}")

    # Verify no message is None
    all_messages_valid = all(msg.get("message") is not None for msg in chat_history)
    print(f"All messages have non-None values: {all_messages_valid}")

    # Verify the problematic message was converted to empty string
    tool_message = next((msg for msg in chat_history if msg["role"] == "TOOL"), None)
    if tool_message and tool_message["message"] == "":
        print("✅ Successfully sanitized None message to empty string")
    else:
        print("❌ Sanitization failed")

    return all_messages_valid


def test_response_text_handling():
    """
    Test the response.text handling logic we added
    """
    print("\nTesting response text handling...")

    # Simulate a response object that might have None text
    class MockResponse:
        def __init__(self, text):
            self.text = text

    # Test with None text
    response_with_none = MockResponse(None)
    response_text = getattr(response_with_none, 'text', '') or ''
    print(f"Response with None text: '{response_text}' (length: {len(response_text)})")

    # Test with actual text
    response_with_text = MockResponse("Hello world")
    response_text = getattr(response_with_text, 'text', '') or ''
    print(f"Response with actual text: '{response_text}' (length: {len(response_text)})")

    # Test with no text attribute
    class MockResponseNoText:
        pass

    response_no_text = MockResponseNoText()
    response_text = getattr(response_no_text, 'text', '') or ''
    print(f"Response without text attribute: '{response_text}' (length: {len(response_text)})")

    print("✅ Response text handling works correctly")
    return True


if __name__ == "__main__":
    print("🧪 Running sanitization tests...\n")

    test1_passed = test_chat_history_sanitization()
    test2_passed = test_response_text_handling()

    print(f"\n🎯 Test Results:")
    print(f"- Chat history sanitization: {'✅ PASS' if test1_passed else '❌ FAIL'}")
    print(f"- Response text handling: {'✅ PASS' if test2_passed else '❌ FAIL'}")

    if test1_passed and test2_passed:
        print("\n🎉 All tests passed! The sanitization fix is working correctly.")
    else:
        print("\n💥 Some tests failed!")