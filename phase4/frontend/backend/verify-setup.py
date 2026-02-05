#!/usr/bin/env python3
"""
Verification script to check if the backend setup is correct
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def verify_env_vars():
    """Verify that required environment variables are set"""
    print("🔍 Checking environment variables...")

    required_vars = ['DATABASE_URL', 'COHERE_API_KEY']
    missing_vars = []

    for var in required_vars:
        if not os.getenv(var):
            missing_vars.append(var)

    if missing_vars:
        print(f"❌ Missing environment variables: {missing_vars}")
        return False
    else:
        print("✅ All required environment variables are set")
        return True

def verify_imports():
    """Verify that all required modules can be imported"""
    print("\n🔍 Checking imports...")

    try:
        import fastapi
        import sqlmodel
        import cohere
        import dotenv
        import pg8000
        print("✅ All required modules can be imported")
        return True
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False

def verify_db_connection():
    """Test database connection"""
    print("\n🔍 Testing database connection...")

    try:
        from sqlmodel import create_engine, Session
        from sqlalchemy import text

        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            print("❌ DATABASE_URL not set")
            return False

        # Create engine and test connection
        engine = create_engine(database_url)

        with Session(engine) as session:
            result = session.exec(text("SELECT 1")).first()
            if result:
                print("✅ Database connection successful")
                return True
            else:
                print("❌ Database connection test failed")
                return False

    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return False

def main():
    print("🚀 Backend Setup Verification")
    print("="*40)

    all_checks_passed = True

    # Check environment variables
    if not verify_env_vars():
        all_checks_passed = False

    # Check imports
    if not verify_imports():
        all_checks_passed = False

    # Check database connection
    if not verify_db_connection():
        all_checks_passed = False

    print("\n" + "="*40)
    if all_checks_passed:
        print("✅ All checks passed! Backend is ready.")
        print("You can now run: uvicorn main:app --reload")
        return 0
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())