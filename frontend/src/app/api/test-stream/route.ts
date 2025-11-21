import { NextResponse } from 'next/server';

export const dynamic = 'force-dynamic';

export async function GET() {
    const encoder = new TextEncoder();
    const customReadable = new ReadableStream({
        async start(controller) {
            try {
                for (let i = 0; i < 5; i++) {
                    const text = `Data chunk ${i}\n`;
                    controller.enqueue(encoder.encode(text));
                    await new Promise((resolve) => setTimeout(resolve, 500));
                }
                controller.close();
            } catch (e) {
                controller.error(e);
            }
        },
    });

    return new NextResponse(customReadable, {
        headers: {
            'Content-Type': 'text/event-stream',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
        },
    });
}
