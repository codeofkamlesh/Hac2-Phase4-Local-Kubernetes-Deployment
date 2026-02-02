---
id: "013"
title: "Implement Recurring Tasks and Date Formatting"
stage: "green"
date_iso: "2026-02-02"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "none"
branch: "001-ai-chat-widget"
user: "kamlesh_kumar"
command: "sp.implement \"The Todo App is functional, but there are critical issues with **Recurring Tasks** and **Date/Time Formatting**.\""
labels: ["frontend", "backend", "tasks", "recurring", "date-formatting", "ui"]
spec: "null"
ticket: "null"
adr: "null"
pr: "null"
files_yaml: |
  - lib/types.ts
  - app/api/tasks/route.ts
  - app/api/tasks/[id]/route.ts
  - app/dashboard/components/TaskCard.tsx
  - app/dashboard/components/TaskModal.tsx
  - scripts/add-recurring-fields.sql
  - package.json
tests_yaml: []
links: []
prompt_text: |
  The Todo App is functional, but there are critical issues with **Recurring Tasks** and **Date/Time Formatting**.

  **1. Recurring Task Feature Implementation:**
   * **Problem:** The "Recurring" option in the "Add Task" modal is not saving to the database, and the recursion pattern is not displayed on the Task Card.
   * **Frontend Requirements:**
       * Ensure the `recurring` (boolean) and `recurrencePattern` (string: 'daily', 'weekly', 'monthly') fields are correctly sent in the POST request payload.
       * **Update Task Card:** Add a small visual indicator (e.g., a "Repeat" icon with the pattern text like "Weekly") on the task card if `recurring` is true.
   * **Backend Requirements (`app/api/tasks/route.ts`):**
       * Ensure the POST endpoint correctly extracts and inserts `recurring` and `recurrencePattern` into the `task` table.

  **2. Date & Time Standardization (Critical):**
   * **Problem:** `createdAt` and `dueDate` are showing incorrect times (likely UTC) or ugly ISO formats.
   * **Requirement:**
       * **Save Logic:** When creating a task, `createdAt` should capture the user's **Local Time**, not server UTC.
       * **Display Logic:** In the Task Card and Dashboard, ALL dates must be formatted as:
           * **Date:** "DD Mon YYYY" (e.g., 02 Feb 2026)
           * **Time:** "hh:mm A" (12-hour format, e.g., 03:30 PM).
       * **Library:** Use `date-fns` or standard `Intl.DateTimeFormat` to ensure consistency.

  **Action Plan:**
  1.  Check and fix the `Task` interface/type to include `recurring` & `recurrencePattern`.
  2.  Update the `AddTaskModal` to capture these fields.
  3.  Update `app/api/tasks/route.ts` to save them.
  4.  Update `TaskCard` component to display the recurrence icon and format the dates as requested (12-hour format).

  Please generate the corrected code for these components.
response_text: |
  Successfully implemented recurring tasks feature and date/time formatting:

  **1. Type Updates (lib/types.ts):**
  - Updated CreateTaskRequest interface to include `recurring` (boolean) and `recurrencePattern` ('daily' | 'weekly' | 'monthly')
  - Updated UpdateTaskRequest interface with the same fields
  - Kept backward compatibility with existing recurring-related fields

  **2. Backend API Updates:**
  - Updated app/api/tasks/route.ts to handle recurring fields in POST and GET requests
  - Updated app/api/tasks/[id]/route.ts to handle recurring fields in PUT and PATCH requests
  - Added proper column handling for "recurring" (BOOLEAN) and "recurrencePattern" (TEXT) in database queries
  - Updated RETURNING clauses to include recurring fields

  **3. Frontend Component Updates:**
  - Updated TaskCard.tsx to display recurrence indicators with proper formatting
  - Updated date formatting to use "DD Mon YYYY, hh:mm A" format (e.g., "02 Feb 2026, 03:30 PM")
  - Updated TaskModal.tsx to capture recurring fields with proper validation
  - Added recurring checkbox and pattern selection dropdown

  **4. Database Schema:**
  - Created SQL script (scripts/add-recurring-fields.sql) to add required columns to task table
  - Added indexes for performance optimization

  **5. Dependencies:**
  - Installed date-fns library for consistent date formatting

  All changes maintain backward compatibility while adding the new functionality.
outcome: "success"
evaluation: "Successfully implemented recurring tasks feature and standardized date/time formatting across the application."
---