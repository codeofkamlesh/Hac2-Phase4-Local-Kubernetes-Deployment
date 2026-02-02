'use client';

import { X, Plus } from 'lucide-react';
import { useState } from 'react';
import { ChatSession } from '@/hooks/useChatSession';

interface TabManagerProps {
  sessions: ChatSession[];
  activeSessionId: string | null;
  onSwitch: (id: string) => void;
  onClose: (id: string) => void;
  onNew: () => void;
}

export default function TabManager({
  sessions,
  activeSessionId,
  onSwitch,
  onClose,
  onNew
}: TabManagerProps) {
  const [editingId, setEditingId] = useState<string | null>(null);
  const [editValue, setEditValue] = useState('');

  const handleRename = async (sessionId: string, newName: string) => {
    if (newName.trim()) {
      try {
        // Update the session title via an API call
        // This would typically call a backend endpoint to update the conversation title
        // For now, we'll just assume the parent component handles the update
        console.log(`Renaming conversation ${sessionId} to ${newName}`);
      } catch (error) {
        console.error('Error renaming conversation:', error);
      }
    }
    setEditingId(null);
  };

  const handleKeyDown = (e: React.KeyboardEvent, sessionId: string) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleRename(sessionId, editValue);
    } else if (e.key === 'Escape') {
      setEditingId(null);
      setEditValue('');
    }
  };

  return (
    <div className="flex overflow-x-auto hide-scrollbar">
      <button
        onClick={onNew}
        className="flex items-center justify-center h-8 w-8 rounded-l-lg bg-gray-100 dark:bg-gray-700 text-gray-600 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600 flex-shrink-0"
        aria-label="New chat"
      >
        <Plus size={16} />
      </button>
      <div className="flex space-x-1">
        {sessions.map((session) => {
          const isActive = session.id === activeSessionId;
          const isEditing = editingId === session.id;

          return (
            <div
              key={session.id}
              className={`flex items-center min-w-[100px] max-w-xs px-2 py-1 rounded-t-lg text-xs font-medium cursor-pointer ${
                isActive
                  ? 'bg-indigo-100 dark:bg-indigo-900 text-indigo-700 dark:text-indigo-200'
                  : 'bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-700'
              }`}
              onClick={() => onSwitch(session.id)}
            >
              {isEditing ? (
                <input
                  type="text"
                  value={editValue}
                  onChange={(e) => setEditValue(e.target.value)}
                  onBlur={() => handleRename(session.id, editValue)}
                  onKeyDown={(e) => handleKeyDown(e, session.id)}
                  autoFocus
                  className="bg-transparent border-b border-gray-400 dark:border-gray-500 outline-none text-xs min-w-[80px] max-w-[120px]"
                  onClick={(e) => e.stopPropagation()}
                />
              ) : (
                <>
                  <span
                    className="truncate mr-1 cursor-pointer"
                    onDoubleClick={() => {
                      setEditingId(session.id);
                      setEditValue(session.title);
                    }}
                  >
                    {session.title}
                  </span>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      onClose(session.id);
                    }}
                    className="ml-1 rounded-full hover:bg-gray-300 dark:hover:bg-gray-600 p-0.5 flex-shrink-0"
                    aria-label={`Close ${session.title}`}
                  >
                    <X size={12} />
                  </button>
                </>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
}