'use client';

import { useState, useRef, useEffect } from 'react';
import { useChat } from '@/hooks/useChat';
import { Send, Loader2, AlertCircle, BrainCircuit } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { ThinkingDrawer } from './ThinkingDrawer';

export function Chat() {
    const { messages, thinkingSteps, sendMessage, isLoading, error } = useChat();
    const [input, setInput] = useState('');
    const [isDrawerOpen, setIsDrawerOpen] = useState(true);
    const messagesEndRef = useRef<HTMLDivElement>(null);
    const inputRef = useRef<HTMLTextAreaElement>(null);

    // Auto-scroll to bottom when new messages arrive
    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [messages]);

    // Auto-open drawer when thinking starts
    useEffect(() => {
        if (isLoading) {
            setIsDrawerOpen(true);
        }
    }, [isLoading]);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!input.trim() || isLoading) return;

        await sendMessage(input);
        setInput('');
        inputRef.current?.focus();
    };

    const handleKeyDown = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSubmit(e);
        }
    };

    return (
        <div className="flex h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 overflow-hidden">
            {/* Main Chat Area */}
            <div className="flex-1 flex flex-col min-w-0">
                {/* Header */}
                <div className="flex-none p-6 bg-black/20 backdrop-blur-lg border-b border-white/10 flex justify-between items-center">
                    <div>
                        <h1 className="text-2xl font-bold text-white">Supply Chain Assistant</h1>
                        <p className="text-sm text-gray-300 mt-1">Ask me anything about suppliers, materials, or BOM</p>
                    </div>
                    <button
                        onClick={() => setIsDrawerOpen(!isDrawerOpen)}
                        className={`p-2 rounded-lg transition-colors ${isDrawerOpen ? 'bg-purple-500/20 text-purple-300' : 'hover:bg-white/10 text-gray-400'
                            }`}
                        title="Toggle Thinking Process"
                    >
                        <BrainCircuit className="w-6 h-6" />
                    </button>
                </div>

                {/* Messages */}
                <div className="flex-1 overflow-y-auto p-6 space-y-4">
                    {messages.length === 0 && (
                        <div className="flex items-center justify-center h-full">
                            <div className="text-center space-y-4">
                                <div className="text-6xl">💬</div>
                                <h2 className="text-xl font-semibold text-white">Start a Conversation</h2>
                                <p className="text-gray-400">Ask me about your supply chain data</p>
                            </div>
                        </div>
                    )}

                    {messages.map((message, index) => (
                        <div
                            key={index}
                            className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                        >
                            <div
                                className={`max-w-[80%] rounded-2xl px-6 py-4 ${message.role === 'user'
                                    ? 'bg-gradient-to-r from-blue-500 to-purple-600 text-white'
                                    : 'bg-white/10 backdrop-blur-lg text-gray-100 border border-white/20'
                                    }`}
                            >
                                {message.role === 'assistant' ? (
                                    <div className="prose prose-invert prose-sm max-w-none">
                                        <ReactMarkdown remarkPlugins={[remarkGfm]}>
                                            {message.content || '_Thinking..._'}
                                        </ReactMarkdown>
                                    </div>
                                ) : (
                                    <p className="whitespace-pre-wrap">{message.content}</p>
                                )}
                            </div>
                        </div>
                    ))}

                    {error && (
                        <div className="flex items-center gap-2 p-4 bg-red-500/20 border border-red-500/50 rounded-lg text-red-200">
                            <AlertCircle className="w-5 h-5 flex-shrink-0" />
                            <p>{error}</p>
                        </div>
                    )}

                    <div ref={messagesEndRef} />
                </div>

                {/* Input */}
                <div className="flex-none p-6 bg-black/20 backdrop-blur-lg border-t border-white/10">
                    <form onSubmit={handleSubmit} className="flex gap-3">
                        <textarea
                            ref={inputRef}
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyDown={handleKeyDown}
                            placeholder="Ask about suppliers, materials, or BOM..."
                            disabled={isLoading}
                            rows={1}
                            className="flex-1 px-4 py-3 bg-white/10 backdrop-blur-sm border border-white/20 rounded-xl 
                       text-white placeholder-gray-400 resize-none focus:outline-none focus:ring-2 
                       focus:ring-purple-500 focus:border-transparent disabled:opacity-50
                       transition-all duration-200"
                        />
                        <button
                            type="submit"
                            disabled={isLoading || !input.trim()}
                            className="px-6 py-3 bg-gradient-to-r from-blue-500 to-purple-600 text-white rounded-xl
                       font-medium disabled:opacity-50 disabled:cursor-not-allowed
                       hover:from-blue-600 hover:to-purple-700 transition-all duration-200
                       flex items-center gap-2 shadow-lg hover:shadow-purple-500/50"
                        >
                            {isLoading ? (
                                <>
                                    <Loader2 className="w-5 h-5 animate-spin" />
                                    <span>Sending...</span>
                                </>
                            ) : (
                                <>
                                    <Send className="w-5 h-5" />
                                    <span>Send</span>
                                </>
                            )}
                        </button>
                    </form>
                </div>
            </div>

            {/* Thinking Drawer */}
            <ThinkingDrawer isOpen={isDrawerOpen} steps={thinkingSteps} />
        </div>
    );
}
