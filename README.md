# Multi Agent AGUI test

## Overview

This repository implements a **multi‑agent AI orchestration platform** built with:

- **Backend**: FastAPI services (materials‑agent, bom‑agent, supplier‑agent, orchestrator) running in Docker containers.
- **Frontend**: Next.js (React) with a custom SSE‑based chat UI and the **Agent Navigator** (formerly Thinking Drawer) that visualises the step‑by‑step execution of agents.
- **LLM Integration**: OpenAI `gpt‑4o‑mini` for orchestration logic and Google Gemini `gemini‑1.5‑flash` for web‑search grounding.

The system demonstrates how autonomous agents can be **registered dynamically**, discovered via a shared protocol, and coordinated by an orchestrator that routes user queries to the appropriate tool.

## Quick Start

```bash
# Clone the repo (already done)
cd google-antigravity-test

# Build and start all services
docker compose up --build -d

# Install frontend dependencies
cd frontend && npm install

# Run the Next.js dev server
npm run dev
```

Open `http://localhost:3000` and interact with the chat UI.

## Key Features

- **Dynamic Agent Registration** – agents expose an `/well‑known/agent.json` endpoint; the orchestrator registers them at startup.
- **Agent Navigator UI** – real‑time timeline of tool calls, merging start/end events via a stable `run_id`.
- **Secure Secrets** – `.env` is ignored; the repository history has been cleaned of API keys.
- **Scalable Architecture** – each agent runs in its own container; the orchestrator can scale horizontally.

## License

MIT License.
