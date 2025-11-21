# Technology Stack & Agent Communication Diagram

```mermaid
flowchart LR
    subgraph Frontend
        FE[React UI Next.js]
    end
    subgraph Orchestrator
        ORCH[FastAPI + LangChain]
        REACT[ReAct LLM Agent]
    end
    subgraph Registry
        REG[AgentCard Registry]
    end
    subgraph Materials Agent
        MAT[FastAPI Service]
        GEM[Google Gemini]
    end
    subgraph BOM Agent
        BOMS[FastAPI Service]
        NEO[Neo4j DB]
    end
    subgraph Supplier Agent
        SUP[FastAPI Service]
        WTO[WTO API]
        WB[World Bank API]
    end
    
    ORCH -->|register/read| REG

    FE -->|SSE Request| ORCH
    ORCH -->|Invokes Tools| REACT
    REACT -->|Tool Call: Materials| MAT
    REACT -->|Tool Call: BOM| BOMS
    REACT -->|Tool Call: Supplier| SUP
    
    MAT -->|Search| GEM
    BOMS -->|Query| NEO
    SUP -->|Fetch Trade Policy| WTO
    SUP -->|Fetch Econ Data| WB
    
    MAT -->|Return Component| ORCH
    BOMS -->|Return Component| ORCH
    SUP -->|Return Component| ORCH
    
    ORCH -->|Stream to UI| FE
```

The diagram illustrates:
- **Frontend** uses Next.js and receives streaming updates via SSE.
- **Orchestrator** runs a FastAPI service with a ReAct‑style LLM executor.
- **Agent Registry** stores `AgentCard` definitions for auto‑discovery.
- Each **Agent** is a FastAPI micro‑service exposing its skills as HTTP endpoints.
- **Materials Agent** leverages Google Gemini for web search.
- **BOM Agent** interacts with a Neo4j graph database.
- **Supplier Agent** calls external WTO and World Bank APIs for risk data.
- All agents return `AGUIComponent` messages (including `run_id`) that the Orchestrator streams back to the Frontend, where the Thinking Drawer merges events.
