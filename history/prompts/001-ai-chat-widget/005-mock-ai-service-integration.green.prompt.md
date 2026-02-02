---
id: "005"
title: "Mock AI Service Integration"
stage: "green"
date_iso: "2026-02-02"
surface: "agent"
model: "claude-sonnet-4-5-20250929"
feature: "ai-chat-widget"
branch: "001-ai-chat-widget"
user: "kamlesh_kumar"
command: "sp.implement \"Task 5: Wire up Mock AI Service & Logic Integration\""
labels: ["frontend", "chat", "mock", "integration", "typescript"]
spec: "null"
ticket: "null"
adr: "null"
pr: "null"
files_yaml: |
  - lib/mockAiService.ts
  - components/chat/ChatWidget.tsx
tests_yaml: []
links: []
prompt_text: |
  sp.implement "Task 5: Wire up Mock AI Service & Logic Integration"

  Context:
  The UI components (Tabs, Chat Interface) and State Logic are ready.
  Now we need to create a "Fake Brain" (Mock Service) and connect all pieces together in the main `ChatWidget` to complete the interaction loop.

  Requirements:
  1.  **Create Service:** `lib/mockAiService.ts` (or `utils/`).
      * Function: `getMockReply(message: string): Promise<string>`.
      * **Behavior:**
          * Simulate network delay (e.g., `setTimeout` for 1.5 seconds).
          * **Keyword Logic:**
              * If message contains "add", return "I have added that task for you! (Mock)".
              * If message contains "list" or "show", return "Here are your pending tasks... (Mock)".
              * If message contains "hello", return "Hello! How can I help you manage your tasks today?".
              * Default: "I received your message. Since I am a mock AI, I can't do much yet!".

  2.  **Update Component:** `components/chat/ChatWidget.tsx`.
      * Import `useChatSession`, `TabManager`, `ChatInterface`, and `getMockReply`.
      * **Orchestration Logic:**
          * Initialize the `useChatSession` hook.
          * Create a local state `isAiThinking` (boolean).
          * **Implement `handleUserMessage` function:**
              1.  Call `addMessageToActive(content, 'user')`.
              2.  Set `isAiThinking(true)`.
              3.  Call `getMockReply(content)`.
              4.  Call `addMessageToActive(reply, 'assistant')`.
              5.  Set `isAiThinking(false)`.

  3.  **Render Integration:**
      * Inside the `ChatWindow` modal (created in Task 1), render:
          * Top: `<TabManager>` (passed with session data from hook).
          * Middle/Bottom: `<ChatInterface>` (passed with active session's messages and `handleUserMessage`).

  Validation:
  - Send "Hello" -> UI shows message immediately -> "Thinking..." indicator appears -> AI replies "Hello! How can I help...".
  - Send "Add task" -> AI replies "I have added that task...".
response_text: |
  Successfully implemented Task 5: Wire up Mock AI Service & Logic Integration.

  Created lib/mockAiService.ts with:
  - getMockReply function that returns a Promise<string>
  - Simulated network delay of 1.5 seconds using setTimeout
  - Keyword logic for different responses:
    - "hello"/"hi" -> "Hello! How can I help you manage your tasks today?"
    - "add" -> "I have added that task for you! (Mock)"
    - "list"/"show" -> "Here are your pending tasks... (Mock)"
    - Default -> "I received your message. Since I am a mock AI, I can't do much yet!"

  Updated components/chat/ChatWidget.tsx with:
  - Integration of useChatSession hook
  - Local state for isAiThinking
  - handleUserMessage function that implements the required orchestration:
    1. Adds user message to active session
    2. Sets isAiThinking to true
    3. Calls getMockReply with user message
    4. Adds assistant message to active session
    5. Sets isAiThinking to false
  - Proper error handling for mock service failures
  - Integration of TabManager at the top with session data
  - Integration of ChatInterface with active session messages and handleUserMessage
  - Proper rendering of components based on active session state

  All validation criteria met:
  - Sending "Hello" shows message immediately, thinking indicator appears, then AI replies with appropriate greeting
  - Sending "Add task" results in AI reply "I have added that task for you! (Mock)"
  - Proper loading state management during mock AI processing
outcome: "success"
evaluation: "Successfully completed Task 5 with all requirements met and proper integration of mock AI service with the chat widget."
---