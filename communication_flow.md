# Communication Flow Protocol (A2A + AGUI)

```mermaid
sequenceDiagram
    title Communication Flow (A2A + AGUI)
    participant User
    participant Frontend
    participant Orchestrator
    participant Registry
    participant Materials_Agent
    participant BOM_Agent
    participant Supplier_Agent
    participant AGUI_Component
    participant External_API

    User->>Frontend: Type query (e.g. "Who supplies Turbocharger?")
    Frontend->>Orchestrator: SSE /chat request (ReAct LLM)
    Orchestrator->>Registry: Load registered AgentCards (auto‑discovery)
    Orchestrator->>Materials_Agent: invoke tool (find‑material) if needed
    Materials_Agent->>External_API: Google Gemini / search
    External_API-->>Materials_Agent: search results
    Materials_Agent-->>Orchestrator: AGUIComponent(type=JSON, id=run1, data={...})
    Orchestrator->>BOM_Agent: get‑bom(part="Turbocharger")
    BOM_Agent-->>Orchestrator: AGUIComponent(type=JSON, id=run2, data={...})
    Orchestrator->>Supplier_Agent: analyze‑risk(supplier, country)
    Supplier_Agent->>External_API: WTO & WorldBank calls
    External_API-->>Supplier_Agent: trade & econ data
    Supplier_Agent-->>Orchestrator: AGUIComponent(type=RISK_CARD, id=run3, data={...})
    Orchestrator->>Frontend: Stream component events (on_tool_start / on_tool_end) with run_id
    Frontend->>AGUI_Component: Render UI (Thinking Drawer) merging events by id
    Frontend->>User: Display final answer and interactive reasoning view
```

The diagram captures:
- **A2A (Agent‑to‑Agent)**: agents register via `AgentCard` and are invoked as tools by the ReAct orchestrator.
- **AGUI**: `AGUIComponent` objects (including the optional `id`) travel from the orchestrator to the frontend, enabling the Thinking Drawer to merge start/end events and present a coherent UI.
