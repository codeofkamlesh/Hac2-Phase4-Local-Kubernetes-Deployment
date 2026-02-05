from sqlmodel import create_engine, Session, text
from typing import Generator
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# For Neon DB with proper SSL configuration
if DATABASE_URL.startswith("postgresql://"):
    # Replace with psycopg for better Neon compatibility if needed
    DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql://", 1)

# Create engine with optimized settings for Neon/PostgreSQL
engine = create_engine(
    DATABASE_URL,
    # Connection pooling settings for serverless environments
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=300,    # Recycle connections after 5 minutes
    echo=False           # Set to True for SQL debugging
)


def get_session() -> Generator[Session, None, None]:
    """
    Dependency to get database session
    """
    with Session(engine) as session:
        yield session


def get_engine():
    """
    Utility function to get the database engine
    """
    return engine


def create_db_and_tables():
    """
    Create all database tables if they don't exist
    """
    from sqlmodel import SQLModel
    # Import models to register them with SQLModel metadata
    from models import User, Task, Conversation, Message
    import sqlalchemy.exc

    try:
        # Create all tables
        SQLModel.metadata.create_all(engine)

        # Try to add the updatedAt column to conversations table if it doesn't exist
        with engine.connect() as conn:
            # Check if column exists first
            try:
                # This query will fail if the column doesn't exist
                conn.execute(text("SELECT \"updatedAt\" FROM conversations LIMIT 1"))
            except sqlalchemy.exc.ProgrammingError:
                # Column doesn't exist, add it
                try:
                    conn.execute(text("ALTER TABLE conversations ADD COLUMN \"updatedAt\" TIMESTAMP DEFAULT NOW()"))
                    conn.commit()
                    print("✅ Added updatedAt column to conversations table")
                except Exception as e:
                    print(f"Info: Could not add updatedAt column (might already exist): {e}")
    except Exception as e:
        print(f"Error creating database tables: {e}")
        raise


def test_connection():
    """
    Test the database connection
    """
    try:
        with Session(engine) as session:
            # Try a simple query to test the connection using text()
            # This fixes the SQLAlchemy 2.0 error
            result = session.exec(text("SELECT 1")).first()
            return result is not None
    except Exception as e:
        print(f"Database connection test failed: {e}")
        return False