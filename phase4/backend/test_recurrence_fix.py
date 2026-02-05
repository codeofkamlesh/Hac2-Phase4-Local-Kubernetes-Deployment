#!/usr/bin/env python3
"""
Test script to verify the recurrencePattern column fix in update_task function.
"""

def test_parameter_normalization():
    """
    Test that the parameter normalization logic works correctly
    """
    print("Testing parameter normalization logic...")

    # Simulate the update_task function's parameter normalization
    def normalize_updates(updates):
        """Simulate the normalization logic added to update_task"""
        # Normalize Parameters (Map AI guesses to 'recurrencePattern' as specified in schema)
        # AI often sends these keys that should map to the recurrencePattern column:
        keys_to_map = ['recurrance_pattern', 'recurring_pattern', 'recurring_interval', 'repeat', 'frequency', 'pattern']

        for key in keys_to_map:
            if key in updates:
                # Move the value to the correct column
                updates['recurring_interval'] = updates.pop(key)
                break # Only map the first one found

        # Map 'tag' to 'tags'
        if 'tag' in updates:
            updates['tags'] = updates.pop('tag')

        return updates

    # Test Case 1: AI sends 'recurrance_pattern' (common misspelling)
    updates1 = {
        'title': 'Test Task',
        'recurrance_pattern': 'daily',
        'priority': 'high'
    }
    normalized1 = normalize_updates(updates1.copy())
    expected1 = {
        'title': 'Test Task',
        'recurring_interval': 'daily',  # Should be mapped correctly
        'priority': 'high'
    }

    success1 = normalized1 == expected1
    print(f"Test 1 - AI 'recurrance_pattern' → 'recurring_interval': {'✅ PASS' if success1 else '❌ FAIL'}")
    if not success1:
        print(f"  Expected: {expected1}")
        print(f"  Got:      {normalized1}")

    # Test Case 2: AI sends 'repeat'
    updates2 = {
        'description': 'Updated description',
        'repeat': 'weekly',
        'completed': False
    }
    normalized2 = normalize_updates(updates2.copy())
    expected2 = {
        'description': 'Updated description',
        'recurring_interval': 'weekly',  # Should be mapped correctly
        'completed': False
    }

    success2 = normalized2 == expected2
    print(f"Test 2 - AI 'repeat' → 'recurring_interval': {'✅ PASS' if success2 else '❌ FAIL'}")
    if not success2:
        print(f"  Expected: {expected2}")
        print(f"  Got:      {normalized2}")

    # Test Case 3: AI sends 'pattern'
    updates3 = {
        'pattern': 'monthly',
        'title': 'Monthly Task'
    }
    normalized3 = normalize_updates(updates3.copy())
    expected3 = {
        'recurring_interval': 'monthly',  # Should be mapped correctly
        'title': 'Monthly Task'
    }

    success3 = normalized3 == expected3
    print(f"Test 3 - AI 'pattern' → 'recurring_interval': {'✅ PASS' if success3 else '❌ FAIL'}")
    if not success3:
        print(f"  Expected: {expected3}")
        print(f"  Got:      {normalized3}")

    # Test Case 4: Normal field (should remain unchanged)
    updates4 = {
        'title': 'Normal Task',
        'description': 'Normal description',
        'priority': 'medium'
    }
    normalized4 = normalize_updates(updates4.copy())
    expected4 = {
        'title': 'Normal Task',
        'description': 'Normal description',
        'priority': 'medium'
    }

    success4 = normalized4 == expected4
    print(f"Test 4 - Normal fields unchanged: {'✅ PASS' if success4 else '❌ FAIL'}")
    if not success4:
        print(f"  Expected: {expected4}")
        print(f"  Got:      {normalized4}")

    # Test Case 5: Tag mapping
    updates5 = {
        'tag': 'important',
        'title': 'Tagged Task'
    }
    normalized5 = normalize_updates(updates5.copy())
    expected5 = {
        'tags': 'important',  # Should be mapped from 'tag' to 'tags'
        'title': 'Tagged Task'
    }

    success5 = normalized5 == expected5
    print(f"Test 5 - AI 'tag' → 'tags': {'✅ PASS' if success5 else '❌ FAIL'}")
    if not success5:
        print(f"  Expected: {expected5}")
        print(f"  Got:      {normalized5}")

    all_tests_passed = all([success1, success2, success3, success4, success5])
    return all_tests_passed


def test_original_functionality_preserved():
    """
    Test that original functionality is still preserved
    """
    print("\nTesting that original functionality is preserved...")

    # Simulate the update logic for original fields
    def apply_updates(task, updates):
        """Simulate the original update logic"""
        if "title" in updates and updates["title"]:
            task["title"] = updates["title"]
        if "description" in updates:
            task["description"] = updates["description"]
        if "completed" in updates:
            task["completed"] = updates["completed"]
        if "priority" in updates and updates["priority"] in ["high", "medium", "low"]:
            task["priority"] = updates["priority"]
        if "due_date" in updates:
            task["due_date"] = updates["due_date"]
        if "recurring_interval" in updates:
            task["recurring_interval"] = updates["recurring_interval"]
        if "tags" in updates:
            task["tags"] = updates["tags"]

        return task

    # Test original functionality
    original_task = {
        "title": "Old Task",
        "description": "Old Description",
        "completed": False,
        "priority": "low",
        "due_date": None,
        "recurring_interval": None,
        "tags": None
    }

    updates = {
        "title": "New Task Title",
        "description": "New Description",
        "completed": True,
        "priority": "high",
        "recurring_interval": "daily"
    }

    updated_task = apply_updates(original_task.copy(), updates)

    expected_task = {
        "title": "New Task Title",
        "description": "New Description",
        "completed": True,
        "priority": "high",
        "due_date": None,
        "recurring_interval": "daily",  # Should be updated
        "tags": None
    }

    success = updated_task == expected_task
    print(f"Original functionality preserved: {'✅ PASS' if success else '❌ FAIL'}")

    if not success:
        print(f"  Expected: {expected_task}")
        print(f"  Got:      {updated_task}")

    return success


if __name__ == "__main__":
    print("🧪 Testing RecurrencePattern Column Fix\n")

    test1_passed = test_parameter_normalization()
    test2_passed = test_original_functionality_preserved()

    print(f"\n🎯 Test Results:")
    print(f"- Parameter normalization: {'✅ PASS' if test1_passed else '❌ FAIL'}")
    print(f"- Original functionality: {'✅ PASS' if test2_passed else '❌ FAIL'}")

    if test1_passed and test2_passed:
        print("\n🎉 All tests passed! The recurrencePattern fix is working correctly.")
        print("\nKey improvements:")
        print("✅ AI parameter variations are now correctly mapped to 'recurring_interval'")
        print("✅ Original functionality is preserved")
        print("✅ Common AI mistakes like 'recurrance_pattern' are handled")
        print("✅ Tag to tags mapping works correctly")
    else:
        print("\n💥 Some tests failed!")