import React from "react";

interface ChatMessageProps {
  message: string;
  isUser: boolean;
}

const ChatMessage: React.FC<ChatMessageProps> = ({ message, isUser }) => {
  return (
    <div
      className={`flex items-end gap-2 ${
        isUser ? "justify-end" : "justify-start"
      } mb-4`}
    >
      {!isUser && (
        <div className="w-8 h-8 bg-blue-200 rounded-full flex items-center justify-center text-blue-700 font-bold text-lg select-none">
          🤖
        </div>
      )}
      <div
        className={`max-w-[70%] rounded-xl px-4 py-3 shadow-md whitespace-pre-line break-words text-base ${
          isUser
            ? "bg-blue-500 text-white rounded-br-md"
            : "bg-gray-200 text-gray-800 rounded-bl-md"
        }`}
      >
        <p>{message}</p>
      </div>
      {isUser && (
        <div className="w-8 h-8 bg-gray-300 rounded-full flex items-center justify-center text-gray-700 font-bold text-lg select-none">
          🧑
        </div>
      )}
    </div>
  );
};

export default ChatMessage;
