import React from 'react';
import { X, CheckCircle, ArrowRight, BrainCircuit } from 'lucide-react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

interface TraceStep {
    tool: string;
    tool_input: any;
    log: string;
    output: string;
}

interface ReasoningDrawerProps {
    isOpen: boolean;
    onClose: () => void;
    trace: TraceStep[];
    isThinking: boolean;
}

export default function ReasoningDrawer({ isOpen, onClose, trace, isThinking }: ReasoningDrawerProps) {
    return (
        <div
            className={`fixed inset-y-0 right-0 w-96 bg-white shadow-2xl transform transition-transform duration-300 ease-in-out z-50 ${isOpen ? 'translate-x-0' : 'translate-x-full'
                }`}
        >
            <div className="h-full flex flex-col">
                {/* Header */}
                <div className="p-4 border-b border-gray-200 flex justify-between items-center bg-blue-50">
                    <div className="flex items-center gap-2 text-blue-700">
                        <BrainCircuit className="w-5 h-5" />
                        <h2 className="font-semibold">Agent Reasoning</h2>
                    </div>
                    <button
                        onClick={onClose}
                        className="p-1 hover:bg-blue-100 rounded-full transition-colors text-gray-500"
                    >
                        <X className="w-5 h-5" />
                    </button>
                </div>

                {/* Content */}
                <div className="flex-1 overflow-y-auto p-4 space-y-6">
                    {trace.length === 0 && !isThinking && (
                        <div className="text-center text-gray-500 mt-10">
                            <p>No reasoning steps available yet.</p>
                            <p className="text-sm mt-2">Ask a complex question to see the agent think!</p>
                        </div>
                    )}

                    {trace.map((step, index) => (
                        <div key={index} className="relative pl-6 border-l-2 border-blue-200 last:border-0">
                            {/* Timeline Dot */}
                            <div className="absolute -left-[9px] top-0 w-4 h-4 rounded-full bg-blue-500 border-2 border-white shadow-sm" />

                            <div className="mb-6">
                                <div className="flex items-center gap-2 mb-2">
                                    <span className="text-xs font-bold uppercase tracking-wider text-blue-600 bg-blue-50 px-2 py-0.5 rounded">
                                        Step {index + 1}
                                    </span>
                                    <span className="font-medium text-gray-900">{step.tool}</span>
                                </div>

                                {/* Input */}
                                <div className="bg-gray-50 rounded-md p-3 mb-2 text-sm">
                                    <div className="text-xs font-semibold text-gray-500 mb-1 uppercase">Input</div>
                                    <pre className="whitespace-pre-wrap text-gray-700 font-mono text-xs">
                                        {JSON.stringify(step.tool_input, null, 2)}
                                    </pre>
                                </div>

                                {/* Output */}
                                <div className="bg-green-50 rounded-md p-3 text-sm border border-green-100">
                                    <div className="flex items-center gap-1 text-xs font-semibold text-green-700 mb-1 uppercase">
                                        <CheckCircle className="w-3 h-3" /> Output
                                    </div>
                                    <div className="text-gray-800 prose prose-sm max-w-none">
                                        {/* Truncate very long outputs for readability */}
                                        <ReactMarkdown remarkPlugins={[remarkGfm]}>
                                            {step.output.length > 300 ? step.output.substring(0, 300) + "..." : step.output}
                                        </ReactMarkdown>
                                    </div>
                                </div>
                            </div>
                        </div>
                    ))}

                    {isThinking && (
                        <div className="flex items-center gap-3 text-gray-500 animate-pulse pl-6 border-l-2 border-blue-200 border-dashed">
                            <div className="absolute -left-[9px] w-4 h-4 rounded-full bg-gray-300 border-2 border-white" />
                            <span className="text-sm">Thinking...</span>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
}
