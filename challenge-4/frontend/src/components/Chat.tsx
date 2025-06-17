import React, { useState, useRef, useEffect } from "react";
import ChatMessage from "./ChatMessage";
import ChatInput from "./ChatInput";

interface Message {
  text: string;
  isUser: boolean;
}

const Chat: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const chatEndRef = useRef<HTMLDivElement | null>(null);

  const sendMessage = async (text: string) => {
    // Add user message to chat
    setMessages((prev) => [...prev, { text, isUser: true }]);
    setIsLoading(true);

    try {
      const response = await fetch(
        "https://ads-chat-bot-479971105418.europe-west1.run.app",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ query: text }),
        }
      );

      const data = await response.json();

      if (response.status === 200) {
        // Add bot response to chat
        setMessages((prev) => [...prev, { text: data.answer, isUser: false }]);
      } else {
        // Handle error response
        setMessages((prev) => [
          ...prev,
          {
            text: `Error: ${data.error || "Something went wrong"}`,
            isUser: false,
          },
        ]);
      }
    } catch (error) {
      // Handle network or other errors
      setMessages((prev) => [
        ...prev,
        { text: "Error: Failed to connect to the server", isUser: false },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className="fixed inset-0 flex flex-col bg-gradient-to-b from-gray-50 to-gray-100">
      <div className="flex-1 overflow-y-auto p-6">
        {messages.length === 0 && (
          <div className="text-center text-gray-400 mt-20 text-lg select-none">
            Start the conversation!
          </div>
        )}
        {messages.map((message, index) => (
          <ChatMessage
            key={index}
            message={message.text}
            isUser={message.isUser}
          />
        ))}
        <div ref={chatEndRef} />
      </div>
      <div className="border-t bg-white/80 backdrop-blur-sm">
        <ChatInput onSendMessage={sendMessage} isLoading={isLoading} />
      </div>
    </div>
  );
};

export default Chat;
