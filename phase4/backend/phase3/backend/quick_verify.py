#!/usr/bin/env python3
"""
Quick verification test for all the core capabilities mentioned in Phase 6.
"""
import subprocess
import sys
import time

def run_command(cmd, desc):
    """Run a command and return success status"""
    print(f"\n🧪 {desc}")
    print(f"   Command: {cmd}")

    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30)
        print(f"   Exit code: {result.returncode}")

        if result.stdout:
            print(f"   Output: {result.stdout[:200]}...")
        if result.stderr:
            print(f"   Error: {result.stderr[:200]}...")

        return result.returncode == 0
    except subprocess.TimeoutExpired:
        print("   ⏱️  Command timed out")
        return False

def main():
    print("🚀 Quick Verification of Phase 6 Robust Tools Implementation")
    print("=" * 60)

    # Test the existing verification scripts
    tests = [
        ("python3 test_robust_tools.py", "Robust Tools Test (ID resolution, date parsing, parameter mapping)"),
        ("python3 test_recurrence_fix.py", "Recurrence Pattern Fix Test"),
        ("python3 -c 'import dateutil.parser; print(\"dateutil available\")'", "Date Util Library Check"),
        ("python3 -c 'from tools import resolve_task_id, add_task, update_task, delete_task, complete_task; print(\"All tools imported successfully\")'", "Tool Imports Check")
    ]

    results = []
    for cmd, desc in tests:
        success = run_command(cmd, desc)
        results.append((desc, success))
        time.sleep(1)  # Small delay between tests

    print(f"\n{'='*60}")
    print("📊 QUICK VERIFICATION RESULTS")
    print("="*60)

    all_passed = True
    for desc, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} - {desc}")
        if not success:
            all_passed = False

    print(f"\n🎯 OVERALL RESULT: {'✅ ALL TESTS PASSED' if all_passed else '❌ SOME TESTS FAILED'}")

    if all_passed:
        print("\n🎉 Phase 6 implementation is working correctly!")
        print("\n✅ All required capabilities verified:")
        print("   • Smart ID resolution (handles both numeric IDs and titles)")
        print("   • Robust date parsing with error handling")
        print("   • Parameter normalization (repeat->recurring_interval, tag->tags, etc.)")
        print("   • Recurrence pattern fixes")
        print("   • All tool functions working properly")
    else:
        print("\n💥 Some verification tests failed")
        print("Check the implementation for the failing components")

    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)