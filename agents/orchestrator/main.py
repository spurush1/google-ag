from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import uvicorn
import os
import json
import asyncio
from typing import List, Dict, Any

from .registry import registry
from shared.protocol import AgentCard, AGUIMessage, AGUIComponent, AGUIComponentType
from .react_agent import get_react_agent

app = FastAPI(title="Orchestrator Agent")

class ChatRequest(BaseModel):
    message: str

@app.post("/register")
def register_agent(agent: AgentCard):
    registry.register_agent(agent)
    return {"status": "registered", "agent": agent.name}

async def generate_stream(message: str):
    agent_executor = get_react_agent()
    if not agent_executor:
        yield json.dumps({"type": "token", "content": "System is initializing. No agents registered yet. Please wait."}) + "\n"
        return

    # Use astream_events to get granular events
    try:
        async for event in agent_executor.astream_events(
            {"input": message}, 
            version="v1"
        ):
            kind = event["event"]
            
            # 1. Stream the final answer tokens
            if kind == "on_chat_model_stream":
                content = event["data"]["chunk"].content
                if content:
                    yield json.dumps({"type": "token", "content": content}) + "\n"
            
            # 2. Stream Tool Usage (Logs)
            elif kind == "on_tool_start":
                tool_name = event["name"]
                tool_input = event["data"].get("input")
                run_id = event.get("run_id")
                
                # Create a log component for the tool start
                log_component = AGUIComponent(
                    type=AGUIComponentType.JSON,
                    title=f"Executing: {tool_name}",
                    data={"input": tool_input, "status": "started"},
                    id=run_id
                )
                yield json.dumps({"type": "component", "component": log_component.model_dump()}) + "\n"

            elif kind == "on_tool_end":
                tool_name = event["name"]
                output = event["data"].get("output")
                run_id = event.get("run_id")
                
                # Create a log component for tool result
                # If output is a stringified JSON (which our agents return for some calls), try to parse it
                display_data = output
                try:
                    if isinstance(output, str):
                        display_data = json.loads(output)
                except:
                    pass

                log_component = AGUIComponent(
                    type=AGUIComponentType.JSON,
                    title=f"Completed: {tool_name}",
                    data={"output": display_data, "status": "completed"},
                    id=run_id
                )
                yield json.dumps({"type": "component", "component": log_component.model_dump()}) + "\n"

    except Exception as e:
        print(f"Stream Error: {e}")
        yield json.dumps({"type": "token", "content": f"\nError: {str(e)}"}) + "\n"

@app.post("/chat")
async def chat(request: ChatRequest):
    return StreamingResponse(generate_stream(request.message), media_type="application/x-ndjson")

@app.get("/health")
def health():
    return {"status": "healthy", "agents": list(registry.agents.keys())}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8003)))
