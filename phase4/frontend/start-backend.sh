#!/bin/bash
# Startup script for the AI Backend

# Load environment variables
export $(grep -v '^#' .env | xargs)

# Navigate to backend directory
cd backend

# Install dependencies if requirements changed
pip install -r requirements.txt

# Run the application
uvicorn main:app --reload --port 8000