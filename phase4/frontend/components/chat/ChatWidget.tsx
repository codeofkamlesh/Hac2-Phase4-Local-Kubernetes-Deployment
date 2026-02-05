'use client';

import { useState, useEffect } from 'react';
import { Bot, X, MessageCircle } from 'lucide-react';
import { useChatSession } from '@/hooks/useChatSession';
import { authClient } from '@/lib/auth-client';
import TabManager from './TabManager';
import ChatInterface from './ChatInterface';

interface ChatWidgetProps {
  refreshTasks?: () => void;
}

export default function ChatWidget({ refreshTasks }: ChatWidgetProps = {}) {
  const [isOpen, setIsOpen] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const {
    sessions,
    activeSessionId,
    createNewSession,
    removeSession,
    switchSession,
    addMessageToActive,
    activeSession
  } = useChatSession();

  // Use the session hook to get current user session
  const { data: session, isPending } = authClient.useSession();

  // Load conversation history when activeSessionId changes
  useEffect(() => {
    const loadConversationHistory = async () => {
      if (activeSessionId && session?.user?.id) {
        try {
          // Assuming there's an API endpoint to fetch conversation messages
          // For now, we'll just use the messages from the session since they're already loaded
          // If you have a specific endpoint for fetching conversation history, use it here
        } catch (error) {
          console.error('Error loading conversation history:', error);
        }
      }
    };

    loadConversationHistory();
  }, [activeSessionId, session]);

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  const handleSendMessage = async (message: string) => {
    // Add user message
    if (activeSessionId) {
      addMessageToActive(message, 'user');

      // Set typing state to true immediately
      setIsTyping(true);

      // Check if user is authenticated using the session hook
      if (!session?.user?.id) {
        addMessageToActive('Error: User not authenticated. Please log in.', 'assistant');
        setIsTyping(false);
        return;
      }

      // Debug log to verify user ID
      console.log("Sending message as User ID:", session.user.id);

      try {
        // Call the Python backend using environment variable
        const apiUrl = process.env.NEXT_PUBLIC_API_URL || 'https://kamlesh-kumar125-hac2-phase4-local-kubernetes-deployment.hf.space';
        const response = await fetch(`${apiUrl}/api/chat`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            message: message,
            user_id: session.user.id,
            conversation_id: activeSessionId // Pass the current conversation ID if available
          }),
        });

        if (!response.ok) {
          throw new Error(`Backend error: ${response.status}`);
        }

        const data = await response.json();

        // Add AI response to the chat
        addMessageToActive(data.response, 'assistant');

        // Refresh tasks if the function was provided
        if (refreshTasks) {
          refreshTasks();
        }
      } catch (error) {
        console.error('Error sending message to backend:', error);
        // Fallback to display error message
        addMessageToActive(`Sorry, there was an error connecting to the AI: ${error}`, 'assistant');
      } finally {
        // Always set typing state to false when done
        setIsTyping(false);
      }
    }
  };

  return (
    <>
      {/* Floating Action Button */}
      <div className="fixed bottom-6 right-6 z-50">
        <button
          onClick={toggleChat}
          className="bg-indigo-600 text-white rounded-full shadow-lg hover:bg-indigo-700 transition-colors duration-200 p-4 flex items-center justify-center w-14 h-14"
          aria-label="Open chat"
        >
          <Bot size={24} />
        </button>
      </div>

      {/* Main Chat Window - No backdrop, floats above content */}
      {isOpen && (
        <div className="fixed bottom-24 right-6 bg-white dark:bg-gray-900 shadow-2xl border border-gray-200 dark:border-gray-700 rounded-lg w-[350px] h-[450px] max-h-[500px] z-40 flex flex-col">
          <div className="flex flex-col h-full">
            {/* Compact Header with TabManager */}
            <div className="border-b border-gray-200 dark:border-gray-700 py-2">
              <TabManager
                sessions={sessions}
                activeSessionId={activeSessionId}
                onSwitch={switchSession}
                onClose={removeSession}
                onNew={createNewSession}
              />
            </div>

            {/* Body with ChatInterface */}
            <div className="flex-grow overflow-hidden p-2">
              {activeSession ? (
                <ChatInterface
                  messages={activeSession.messages}
                  onSendMessage={handleSendMessage}
                  isLoading={false}
                  isTyping={isTyping}
                />
              ) : (
                <div className="flex items-center justify-center h-full text-gray-500 dark:text-gray-400">
                  <p>No active session</p>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </>
  );
}