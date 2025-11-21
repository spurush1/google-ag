'use client';

import { useState, useRef, useCallback } from 'react';

export interface Message {
    role: 'user' | 'assistant';
    content: string;
}

export interface ThinkingStep {
    id: string;
    title: string;
    type: 'json';
    data: any;
    status: 'started' | 'completed';
    timestamp: number;
}

export function useChat() {
    const [messages, setMessages] = useState<Message[]>([]);
    const [thinkingSteps, setThinkingSteps] = useState<ThinkingStep[]>([]);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const abortControllerRef = useRef<AbortController | null>(null);

    const sendMessage = useCallback(async (text: string) => {
        if (!text.trim()) return;

        // Add user message
        const userMessage: Message = { role: 'user', content: text };
        setMessages((prev) => [...prev, userMessage]);

        // Initialize thinking steps with "Received request"
        setThinkingSteps([{
            id: 'init-' + Date.now(),
            title: 'Orchestrator: Received request',
            type: 'json',
            data: { message: 'Processing user query...', timestamp: new Date().toISOString() },
            status: 'completed',
            timestamp: Date.now()
        }]);

        setIsLoading(true);
        setError(null);

        // Create abort controller for this request
        abortControllerRef.current = new AbortController();

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text }),
                signal: abortControllerRef.current.signal,
            });

            if (!response.ok) {
                throw new Error(`HTTP ${response.status}: ${response.statusText}`);
            }

            if (!response.body) {
                throw new Error('No response body');
            }

            // Read SSE stream
            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let buffer = '';
            let assistantContent = '';

            // Add empty assistant message that we'll update
            setMessages(prev => [...prev, { role: 'assistant', content: '' }]);

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                buffer += decoder.decode(value, { stream: true });
                const lines = buffer.split('\n');
                buffer = lines.pop() || '';

                for (const line of lines) {
                    if (!line.trim() || line === '[DONE]') continue;

                    // Parse SSE format
                    const jsonLine = line.startsWith('data: ') ? line.substring(6) : line;

                    try {
                        const event = JSON.parse(jsonLine);

                        // Handle text tokens
                        if (event.type === 'token' && event.content) {
                            assistantContent += event.content;
                            setMessages((prev) => {
                                const newMessages = [...prev];
                                newMessages[newMessages.length - 1] = {
                                    role: 'assistant',
                                    content: assistantContent,
                                };
                                return newMessages;
                            });
                        }

                        // Handle thinking/component events
                        else if (event.type === 'component' && event.component) {
                            const component = event.component;

                            // Map tool names to friendly agent descriptions
                            let friendlyTitle = component.title || 'Processing...';

                            if (friendlyTitle.includes('find-material')) {
                                friendlyTitle = friendlyTitle.replace('Executing: find-material', 'Materials Agent: Searching for material details')
                                    .replace('Completed: find-material', 'Materials Agent: Found material details');
                            } else if (friendlyTitle.includes('analyze-risk')) {
                                friendlyTitle = friendlyTitle.replace('Executing: analyze-risk', 'Supplier Agent: Analyzing geopolitical risk')
                                    .replace('Completed: analyze-risk', 'Supplier Agent: Risk analysis complete');
                            } else if (friendlyTitle.includes('get-bom')) {
                                friendlyTitle = friendlyTitle.replace('Executing: get-bom', 'BOM Agent: Retrieving Bill of Materials')
                                    .replace('Completed: get-bom', 'BOM Agent: BOM retrieval complete');
                            } else if (friendlyTitle.includes('tavily')) {
                                friendlyTitle = friendlyTitle.replace('Executing: tavily', 'Web Search: Searching external sources')
                                    .replace('Completed: tavily', 'Web Search: Search complete');
                            }

                            setThinkingSteps((prev) => {
                                // If we have an ID, try to find and update existing step
                                if (component.id) {
                                    const existingIndex = prev.findIndex(step => step.id === component.id);
                                    if (existingIndex !== -1) {
                                        const newSteps = [...prev];
                                        newSteps[existingIndex] = {
                                            ...newSteps[existingIndex],
                                            title: friendlyTitle,
                                            status: component.data?.status || 'completed',
                                            data: { ...newSteps[existingIndex].data, ...component.data }
                                        };
                                        return newSteps;
                                    }
                                    // If ID exists but step doesn't, fall through to add new
                                }

                                const newStep: ThinkingStep = {
                                    id: component.id || Date.now().toString() + Math.random().toString(),
                                    title: friendlyTitle,
                                    type: component.type || 'json',
                                    data: component.data || {},
                                    status: component.data?.status || 'completed',
                                    timestamp: Date.now()
                                };
                                return [...prev, newStep];
                            });
                        }
                    } catch (e) {
                        // Skip invalid JSON
                        console.warn('Failed to parse SSE line:', line);
                    }
                }
            }
        } catch (err: any) {
            if (err.name === 'AbortError') {
                console.log('Request cancelled');
                return;
            }

            console.error('Chat error:', err);
            setError(err.message || 'Failed to send message');

            // Remove the empty assistant message if error occurred
            setMessages((prev) => {
                const newMessages = [...prev];
                if (newMessages.length > 0 && newMessages[newMessages.length - 1].role === 'assistant' && !newMessages[newMessages.length - 1].content) {
                    newMessages.pop();
                }
                return newMessages;
            });
        } finally {
            setIsLoading(false);
            abortControllerRef.current = null;
        }
    }, []);

    const cancelRequest = useCallback(() => {
        if (abortControllerRef.current) {
            abortControllerRef.current.abort();
            abortControllerRef.current = null;
            setIsLoading(false);
        }
    }, []);

    return {
        messages,
        thinkingSteps,
        sendMessage,
        isLoading,
        error,
        cancelRequest,
    };
}
