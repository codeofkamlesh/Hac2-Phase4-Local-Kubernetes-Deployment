---
id: "008"
title: "Reset Better Auth Schema"
stage: "green"
date_iso: "2026-02-02"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "001-ai-chat-widget"
user: "kamlesh_kumar"
command: "sp.implement \"The current database schema in Neon DB has naming conflicts (snake_case vs camelCase) causing repeated errors with Better Auth. Since this is a development environment, I want to RESET the database completely to match Better Auth's default camelCase schema.\""
labels: ["database", "auth", "better-auth", "postgres", "neon", "reset", "schema"]
spec: "null"
ticket: "null"
adr: "null"
pr: "null"
files_yaml: |
  - scripts/reset-better-auth-schema.sql
tests_yaml: []
links: []
prompt_text: |
  The current database schema in Neon DB has naming conflicts (snake_case vs camelCase) causing repeated errors with Better Auth.
  Since this is a development environment, I want to RESET the database completely to match Better Auth's default camelCase schema.

  Please provide a SQL script that I can run in the Neon Console to:
  1. DROP the existing tables (`user`, `users`, `session`, `sessions`, `account`, `accounts`, `verification`, `verification_tokens`) to clear the mess.
  2. CREATE the tables again using the strict **CamelCase** column names expected by Better Auth defaults.

  The Schema should strictly look like this:

  -- User Table
  CREATE TABLE "user" (
      id TEXT PRIMARY KEY,
      name TEXT NOT NULL,
      email TEXT NOT NULL UNIQUE,
      "emailVerified" BOOLEAN NOT NULL,
      image TEXT,
      "createdAt" TIMESTAMP NOT NULL,
      "updatedAt" TIMESTAMP NOT NULL
  );

  -- Session Table
  CREATE TABLE "session" (
      id TEXT PRIMARY KEY,
      "expiresAt" TIMESTAMP NOT NULL,
      token TEXT NOT NULL UNIQUE,
      "createdAt" TIMESTAMP NOT NULL,
      "updatedAt" TIMESTAMP NOT NULL,
      "ipAddress" TEXT,
      "userAgent" TEXT,
      "userId" TEXT NOT NULL REFERENCES "user"(id) ON DELETE CASCADE
  );

  -- Account Table
  CREATE TABLE "account" (
      id TEXT PRIMARY KEY,
      "accountId" TEXT NOT NULL,
      "providerId" TEXT NOT NULL,
      "userId" TEXT NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
      "accessToken" TEXT,
      "refreshToken" TEXT,
      "idToken" TEXT,
      "accessTokenExpiresAt" TIMESTAMP,
      "refreshTokenExpiresAt" TIMESTAMP,
      scope TEXT,
      password TEXT,
      "createdAt" TIMESTAMP NOT NULL,
      "updatedAt" TIMESTAMP NOT NULL
  );

  -- Verification Table
  CREATE TABLE "verification" (
      id TEXT PRIMARY KEY,
      identifier TEXT NOT NULL,
      value TEXT NOT NULL,
      "expiresAt" TIMESTAMP NOT NULL,
      "createdAt" TIMESTAMP,
      "updatedAt" TIMESTAMP
  );

  Please confirm this SQL is correct and tell me to run it in the Neon SQL Editor.
response_text: |
  Successfully created a comprehensive SQL script to reset the Better Auth schema with camelCase columns:

  1. Created reset-better-auth-schema.sql with:
     - DROP statements for all possible legacy table variations (users, sessions, accounts, verification_tokens, user, session, account, verification)
     - CREATE TABLE statements with exact camelCase column names as requested
     - Proper foreign key constraints and cascading deletes
     - DEFAULT values for timestamps (NOW())
     - Performance indexes for commonly queried columns
     - A confirmation message when the script completes

  2. The script follows the exact schema provided in the requirements with camelCase column names like "emailVerified", "createdAt", "updatedAt", etc.

  3. The script includes CASCADE for foreign key relationships to ensure clean drops.

  To use: Copy the content of scripts/reset-better-auth-schema.sql and run it in the Neon Console SQL Editor.
outcome: "success"
evaluation: "Successfully created a comprehensive SQL script to reset Better Auth schema with camelCase columns as requested."
---