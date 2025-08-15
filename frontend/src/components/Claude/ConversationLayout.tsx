import React, { useRef, useEffect, useState } from 'react';
import ClaudeMessage from './ClaudeMessage.tsx';
import ClaudeInputArea from './ClaudeInputArea.tsx';
import TypingIndicator from './TypingIndicator.tsx';

interface Message {
  id: number;
  type: 'user' | 'assistant';
  content: string;
  timestamp: string;
}

type TypingStage = 'thinking' | 'analyzing' | 'processing' | 'generating';

interface ConversationLayoutProps {
  messages: Message[];
  inputValue: string;
  setInputValue: (value: string) => void;
  onSendMessage: (message: string, fileId?: string) => void;
  isTyping?: boolean;
  typingStage?: TypingStage;
  addMessage?: (message: any) => void;
}

const ConversationLayout: React.FC<ConversationLayoutProps> = ({ 
  messages, 
  inputValue, 
  setInputValue, 
  onSendMessage,
  isTyping = false,
  typingStage = 'thinking',
  addMessage
}) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const [currentFileId, setCurrentFileId] = useState<string | undefined>();
  
  const handleFileUploaded = (fileId: string, fileName: string) => {
    // Store the file ID for subsequent messages
    setCurrentFileId(fileId);
    
    // Automatically send a message to analyze the uploaded file
    const analysisMessage = `Analyze the uploaded file: ${fileName}`;
    onSendMessage(analysisMessage, fileId);
  };
  
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);
  
  return (
    <div className="flex flex-col h-full">
      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto min-h-0">
        <div className="max-w-3xl mx-auto px-6 py-8">
          <div className="space-y-8">
            {messages.map((message) => (
              <ClaudeMessage key={message.id} message={message} />
            ))}
            
            {isTyping && <TypingIndicator stage={typingStage} />}
            <div ref={messagesEndRef} />
          </div>
        </div>
      </div>
      
      {/* Bottom Input */}
      <div className="bg-[var(--bg-main)] flex-shrink-0">
        <div className="max-w-3xl mx-auto px-6 py-3">
          <ClaudeInputArea
            inputValue={inputValue}
            setInputValue={setInputValue}
            onSend={(fileId?: string) => {
              // If typing, this will trigger stop functionality in onSendMessage
              // If not typing, this will send the message
              // Use the provided fileId or the stored currentFileId
              onSendMessage(inputValue, fileId || currentFileId);
            }}
            isTyping={isTyping}
            onFileUploaded={handleFileUploaded}
            addMessage={addMessage}
          />
        </div>
      </div>
    </div>
  );
};

export default ConversationLayout; 