import { ThinkingStep } from '@/hooks/useChat';
import { CheckCircle2, Loader2, ChevronRight, ChevronDown, Terminal, Activity } from 'lucide-react';
import { useState, useRef, useEffect } from 'react';

interface ThinkingDrawerProps {
    isOpen: boolean;
    steps: ThinkingStep[];
}

export function ThinkingDrawer({ isOpen, steps }: ThinkingDrawerProps) {
    const bottomRef = useRef<HTMLDivElement>(null);

    // Auto-scroll to bottom when steps change
    useEffect(() => {
        if (isOpen) {
            bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
        }
    }, [steps, isOpen]);

    if (!isOpen) return null;

    return (
        <div className="w-96 border-l border-white/10 bg-black/20 backdrop-blur-xl flex flex-col h-full transition-all duration-300 shadow-2xl">
            <div className="p-4 border-b border-white/10 bg-white/5">
                <h2 className="text-lg font-semibold text-white flex items-center gap-2">
                    <Activity className="w-5 h-5 text-purple-400" />
                    Agent Navigator
                </h2>
                <p className="text-xs text-gray-400 mt-1">Real-time orchestration timeline</p>
            </div>

            <div className="flex-1 overflow-y-auto p-4 space-y-6 relative">
                {/* Vertical Timeline Line */}
                {steps.length > 0 && (
                    <div className="absolute left-[27px] top-8 bottom-8 w-0.5 bg-white/10 -z-10" />
                )}

                {steps.length === 0 ? (
                    <div className="text-center text-gray-500 mt-10">
                        <p>Ready to navigate.</p>
                        <p className="text-xs mt-2">Start a chat to track agent actions.</p>
                    </div>
                ) : (
                    steps.map((step, index) => (
                        <ThinkingStepItem key={step.id} step={step} isLast={index === steps.length - 1} />
                    ))
                )}
                <div ref={bottomRef} />
            </div>
        </div>
    );
}

function ThinkingStepItem({ step, isLast }: { step: ThinkingStep; isLast: boolean }) {
    const [isExpanded, setIsExpanded] = useState(false);
    const isCompleted = step.status === 'completed';

    // Auto-expand the last active step if it's not completed (optional, but nice)
    // useEffect(() => { if (!isCompleted && isLast) setIsExpanded(true); }, [isCompleted, isLast]);

    return (
        <div className="relative z-10">
            <div className={`rounded-lg border transition-all duration-300 overflow-hidden ${isCompleted
                    ? 'bg-white/5 border-white/10 hover:bg-white/10'
                    : 'bg-purple-500/10 border-purple-500/30 shadow-[0_0_15px_rgba(168,85,247,0.2)]'
                }`}>
                <button
                    onClick={() => setIsExpanded(!isExpanded)}
                    className="w-full flex items-center gap-3 p-3 text-left"
                >
                    <div className={`flex-shrink-0 rounded-full p-1 ${isCompleted ? 'bg-green-500/20' : 'bg-purple-500/20'
                        }`}>
                        {isCompleted ? (
                            <CheckCircle2 className="w-4 h-4 text-green-400" />
                        ) : (
                            <Loader2 className="w-4 h-4 text-purple-400 animate-spin" />
                        )}
                    </div>

                    <div className="flex-1 min-w-0">
                        <p className={`text-sm font-medium truncate ${isCompleted ? 'text-gray-300' : 'text-purple-200'
                            }`}>
                            {step.title}
                        </p>
                        <p className="text-xs text-gray-500">
                            {isCompleted ? 'Completed' : 'In Progress...'}
                        </p>
                    </div>

                    {isExpanded ? (
                        <ChevronDown className="w-4 h-4 text-gray-500" />
                    ) : (
                        <ChevronRight className="w-4 h-4 text-gray-500" />
                    )}
                </button>

                {isExpanded && (
                    <div className="p-3 pt-0 border-t border-white/5 bg-black/20 animate-in slide-in-from-top-2 duration-200">
                        <pre className="text-[10px] text-gray-300 overflow-x-auto p-2 rounded bg-black/40 font-mono custom-scrollbar">
                            {JSON.stringify(step.data, null, 2)}
                        </pre>
                    </div>
                )}
            </div>
        </div>
    );
}
