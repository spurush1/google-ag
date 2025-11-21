import { NextRequest, NextResponse } from 'next/server';

export async function POST(req: NextRequest) {
    try {
        const { message } = await req.json();

        if (!message) {
            return NextResponse.json({ error: 'Message is required' }, { status: 400 });
        }

        const orchestratorUrl = process.env.NEXT_PUBLIC_ORCHESTRATOR_URL || 'http://orchestrator:8003';

        console.log('=== Chat API Route ===');
        console.log('User message:', message.substring(0, 100));
        console.log('Forwarding to:', `${orchestratorUrl}/chat`);

        const response = await fetch(`${orchestratorUrl}/chat`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message }),
        });

        if (!response.ok) {
            const errorText = await response.text();
            console.error('Orchestrator error:', response.status, errorText);
            return NextResponse.json(
                { error: `Orchestrator error: ${response.status}` },
                { status: response.status }
            );
        }

        if (!response.body) {
            return NextResponse.json({ error: 'No response from orchestrator' }, { status: 500 });
        }

        // Stream the SSE response back to the client
        return new NextResponse(response.body, {
            headers: {
                'Content-Type': 'text/event-stream',
                'Cache-Control': 'no-cache, no-transform',
                'Connection': 'keep-alive',
                'X-Accel-Buffering': 'no',
            },
        });

    } catch (error: any) {
        console.error('Chat API error:', error);
        return NextResponse.json(
            { error: 'Internal server error', details: error.message },
            { status: 500 }
        );
    }
}
