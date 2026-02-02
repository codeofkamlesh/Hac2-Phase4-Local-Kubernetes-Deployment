'use client';

import { useState } from 'react';
import { Bot } from 'lucide-react';
import { useChatSession } from '@/hooks/useChatSession';
import TabManager from './TabManager';
import ChatInterface from './ChatInterface';
import { getMockReply } from '@/lib/mockAiService';

export default function ChatWidget() {
  const [isVisible, setIsVisible] = useState(false);
  const [isAiThinking, setIsAiThinking] = useState(false);

  const {
    sessions,
    activeSessionId,
    createNewSession,
    removeSession,
    switchSession,
    addMessageToActive,
    activeSession
  } = useChatSession();

  const toggleVisibility = () => {
    setIsVisible(!isVisible);
  };

  const handleUserMessage = async (content: string) => {
    // Add user message immediately
    addMessageToActive(content, 'user');

    // Set AI thinking state
    setIsAiThinking(true);

    try {
      // Get mock reply
      const reply = await getMockReply(content);

      // Add assistant message
      addMessageToActive(reply, 'assistant');
    } catch (error) {
      // In case of error, add an error message
      addMessageToActive("Sorry, I encountered an error processing your request.", 'assistant');
    } finally {
      // Reset AI thinking state
      setIsAiThinking(false);
    }
  };

  return (
    <div className="fixed bottom-6 right-6 z-50">
      {/* Floating Action Button */}
      <button
        onClick={toggleVisibility}
        className="bg-indigo-600 text-white rounded-full shadow-lg hover:bg-indigo-700 transition-colors duration-200 p-4 flex items-center justify-center w-14 h-14"
        aria-label="Open chat"
      >
        <Bot size={24} />
      </button>

      {/* Backdrop when chat is open */}
      {isVisible && (
        <div
          className="fixed inset-0 bg-black bg-opacity-30 z-40"
          onClick={toggleVisibility}
        ></div>
      )}

      {/* Chat Window Container */}
      {isVisible && (
        <div
          className="fixed inset-0 bg-white dark:bg-gray-900 rounded-none shadow-2xl border-0 z-50 flex flex-col sm:rounded-xl sm:border border-gray-200 dark:border-gray-700 sm:inset-auto sm:bottom-20 sm:right-6 sm:w-[380px] sm:h-[600px] max-w-[calc(100vw-2rem)] max-h-[calc(100vh-5rem)]"
          onClick={(e) => e.stopPropagation()}
        >
          <div className="flex flex-col h-full">
            {/* Tab Manager at the top */}
            <div className="border-b border-gray-200 dark:border-gray-700">
              <TabManager
                sessions={sessions}
                activeSessionId={activeSessionId}
                onSwitch={switchSession}
                onClose={removeSession}
                onNew={createNewSession}
              />
            </div>

            {/* Chat Interface in the middle/bottom */}
            <div className="flex-grow overflow-hidden">
              {activeSession ? (
                <ChatInterface
                  messages={activeSession.messages}
                  onSendMessage={handleUserMessage}
                  isLoading={isAiThinking}
                />
              ) : (
                <div className="flex items-center justify-center h-full text-gray-500 dark:text-gray-400">
                  <p>No active session. Create a new chat to start.</p>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}