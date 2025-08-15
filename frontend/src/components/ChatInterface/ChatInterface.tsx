import React, { useState, useRef, useEffect } from 'react';
import DataSophLogo from '../DataSophLogo';
import { AIMessage } from '../UI/MessageParser';
import { Message } from '../../types/chat.ts';

interface ChatInterfaceProps {
  messages: Message[];
  onSendMessage: (message: string, files?: FileList) => void;
  isLoading: boolean;
  className?: string;
}

const ChatInterface: React.FC<ChatInterfaceProps> = ({
  messages,
  onSendMessage,
  isLoading,
  className = ''
}) => {
  const [input, setInput] = useState('');
  const [isDragOver, setIsDragOver] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (input.trim() && !isLoading) {
      onSendMessage(input.trim());
      setInput('');
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragOver(false);
    
    const files = e.dataTransfer.files;
    if (files.length > 0) {
      onSendMessage(input.trim() || "I've uploaded some data for analysis", files);
      setInput('');
    }
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files.length > 0) {
      onSendMessage(input.trim() || "I've uploaded some data for analysis", files);
      setInput('');
    }
  };

  if (messages.length === 0) {
    return (
      <div className={`flex flex-col h-full ${className}`}>
        {/* Welcome Screen */}
        <div className="flex-1 flex items-center justify-center p-8">
          <div className="max-w-2xl text-center space-y-8">
            {/* Professional Logo and Greeting */}
            <div className="space-y-4">
              <DataSophLogo variant="default" className="mx-auto" />
              
              <div className="space-y-3">
                <h1 className="text-3xl font-bold text-gray-900">
                  Welcome to Datasoph
                </h1>
                <p className="text-lg text-gray-600 max-w-xl mx-auto">
                  Your PhD-level data science partner with 15+ years of Fortune 500 experience. 
                  I think like a consultant, communicate like a professor, and deliver like a professional analytics team.
                </p>
              </div>
            </div>

            {/* Professional Capabilities */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-12">
              <div className="bg-white border border-gray-200 rounded-lg p-6 text-left">
                <div className="flex items-center space-x-3 mb-3">
                  <div className="w-8 h-8 bg-blue-100 rounded-lg flex items-center justify-center">
                    <svg className="w-4 h-4 text-blue-600" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M3 3a1 1 0 000 2v8a2 2 0 002 2h2.586l-1.293 1.293a1 1 0 101.414 1.414L10 15.414l2.293 2.293a1 1 0 001.414-1.414L12.414 15H15a2 2 0 002-2V5a1 1 0 100-2H3zm11.707 4.707a1 1 0 00-1.414-1.414L10 9.586 8.707 8.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <h3 className="font-semibold text-gray-900">Statistical Analysis</h3>
                </div>
                <p className="text-sm text-gray-600">
                  PhD-level hypothesis testing with effect sizes, confidence intervals, and ASA compliance
                </p>
              </div>

              <div className="bg-white border border-gray-200 rounded-lg p-6 text-left">
                <div className="flex items-center space-x-3 mb-3">
                  <div className="w-8 h-8 bg-green-100 rounded-lg flex items-center justify-center">
                    <svg className="w-4 h-4 text-green-600" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                    </svg>
                  </div>
                  <h3 className="font-semibold text-gray-900">Machine Learning</h3>
                </div>
                <p className="text-sm text-gray-600">
                  Production-ready ML pipelines with business ROI focus and deployment strategies
                </p>
              </div>

              <div className="bg-white border border-gray-200 rounded-lg p-6 text-left">
                <div className="flex items-center space-x-3 mb-3">
                  <div className="w-8 h-8 bg-purple-100 rounded-lg flex items-center justify-center">
                    <svg className="w-4 h-4 text-purple-600" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M2 6a2 2 0 012-2h4l2 2h4a2 2 0 012 2v6a2 2 0 01-2 2H4a2 2 0 01-2-2V6zm4.707 4.293a1 1 0 00-1.414 1.414L7 13.414l3.293-3.293a1 1 0 00-1.414-1.414L7 10.586 6.707 10.293z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <h3 className="font-semibold text-gray-900">Business Intelligence</h3>
                </div>
                <p className="text-sm text-gray-600">
                  Executive-level strategic recommendations with financial impact modeling
                </p>
              </div>

              <div className="bg-white border border-gray-200 rounded-lg p-6 text-left">
                <div className="flex items-center space-x-3 mb-3">
                  <div className="w-8 h-8 bg-orange-100 rounded-lg flex items-center justify-center">
                    <svg className="w-4 h-4 text-orange-600" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1zm0 4a1 1 0 011-1h12a1 1 0 110 2H4a1 1 0 01-1-1z" clipRule="evenodd" />
                    </svg>
                  </div>
                  <h3 className="font-semibold text-gray-900">Professional Reporting</h3>
                </div>
                <p className="text-sm text-gray-600">
                  Production-ready code with comprehensive documentation and enterprise standards
                </p>
              </div>
            </div>

            {/* Getting Started */}
            <div className="bg-blue-50 border border-blue-200 rounded-lg p-6">
              <h3 className="font-semibold text-blue-900 mb-3">Ready to Begin?</h3>
              <div className="text-sm text-blue-800 space-y-2">
                <p><strong>Upload your data</strong> for immediate comprehensive analysis</p>
                <p><strong>Ask me anything</strong> about statistical analysis, ML modeling, or business intelligence</p>
                <p><strong>Get professional insights</strong> with Fortune 500 standards and academic rigor</p>
              </div>
            </div>
          </div>
        </div>

        {/* Input Area */}
        <div className="border-t border-gray-200 p-4 bg-white">
          <form onSubmit={handleSubmit} className="max-w-4xl mx-auto">
            <div className="relative">
              <textarea
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Ask me about statistical analysis, machine learning, or upload your data for professional analysis..."
                className="w-full p-4 pr-24 border border-gray-300 rounded-lg resize-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                rows={3}
                disabled={isLoading}
              />
              
              <div className="absolute bottom-3 right-3 flex items-center space-x-2">
                <button
                  type="button"
                  onClick={() => fileInputRef.current?.click()}
                  className="p-2 text-gray-400 hover:text-gray-600 rounded-md hover:bg-gray-100 transition-colors"
                  title="Upload data file"
                >
                  <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" />
                  </svg>
                </button>
                
                <button
                  type="submit"
                  disabled={!input.trim() || isLoading}
                  className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                >
                  {isLoading ? (
                    <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                  ) : (
                    <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                    </svg>
                  )}
                </button>
              </div>
              
              <input
                ref={fileInputRef}
                type="file"
                onChange={handleFileSelect}
                accept=".csv,.xlsx,.xls,.json,.txt,.pdf,.png,.jpg,.jpeg,.tiff,.tif,.bmp,.webp,.heic,.svg"
                className="hidden"
                multiple
              />
            </div>
          </form>
        </div>
      </div>
    );
  }

  return (
    <div 
      className={`flex flex-col h-full ${className} ${isDragOver ? 'bg-blue-50 border-2 border-dashed border-blue-300' : ''}`}
      onDragOver={handleDragOver}
      onDragLeave={handleDragLeave}
      onDrop={handleDrop}
    >
      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
                 {messages.map((message) => (
           <div key={message.id} className={`flex ${message.isUser ? 'justify-end' : 'justify-start'}`}>
             <div className={`max-w-4xl ${message.isUser ? 'ml-12' : 'mr-12'}`}>
               {!message.isUser && (
                                 <div className="flex items-center space-x-2 mb-2">
                  <DataSophLogo variant="icon-only" />
                  <span className="text-sm font-medium text-gray-700">Datasoph</span>
                  <span className="text-xs text-gray-500">PhD-Level Analysis</span>
                </div>
               )}
               
               <div className={`rounded-lg p-4 ${
                 message.isUser 
                   ? 'bg-blue-600 text-white' 
                   : 'bg-white border border-gray-200'
               }`}>
                 {!message.isUser ? (
                   <AIMessage content={message.content} />
                 ) : (
                   <p className="whitespace-pre-wrap">{message.content}</p>
                 )}
               </div>
              
              <div className="mt-1 text-xs text-gray-500">
                {new Date(message.timestamp).toLocaleTimeString()}
              </div>
            </div>
          </div>
        ))}
        
        {isLoading && (
          <div className="flex justify-start">
            <div className="max-w-4xl mr-12">
              <div className="flex items-center space-x-2 mb-2">
                <DataSophLogo variant="icon-only" />
                <span className="text-sm font-medium text-gray-700">Datasoph</span>
                <span className="text-xs text-gray-500">Analyzing...</span>
              </div>
              
              <div className="bg-white border border-gray-200 rounded-lg p-4">
                <div className="flex items-center space-x-2">
                  <div className="flex space-x-1">
                    <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                    <div className="w-2 h-2 bg-blue-600 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                  </div>
                  <span className="text-sm text-gray-600">Performing PhD-level analysis...</span>
                </div>
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="border-t border-gray-200 p-4 bg-white">
        <form onSubmit={handleSubmit} className="max-w-4xl mx-auto">
          <div className="relative">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Continue the conversation with your PhD-level data science partner..."
              className="w-full p-4 pr-24 border border-gray-300 rounded-lg resize-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              rows={2}
              disabled={isLoading}
            />
            
            <div className="absolute bottom-3 right-3 flex items-center space-x-2">
              <button
                type="button"
                onClick={() => fileInputRef.current?.click()}
                className="p-2 text-gray-400 hover:text-gray-600 rounded-md hover:bg-gray-100 transition-colors"
                title="Upload additional data"
              >
                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" />
                </svg>
              </button>
              
              <button
                type="submit"
                disabled={!input.trim() || isLoading}
                className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                {isLoading ? (
                  <div className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
                ) : (
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
                  </svg>
                )}
              </button>
            </div>
            
            <input
              ref={fileInputRef}
              type="file"
              onChange={handleFileSelect}
              accept=".csv,.xlsx,.xls,.json,.txt,.pdf,.png,.jpg,.jpeg,.tiff,.tif,.bmp,.webp,.heic,.svg"
              className="hidden"
              multiple
            />
          </div>
        </form>
      </div>
    </div>
  );
};

export default ChatInterface; 