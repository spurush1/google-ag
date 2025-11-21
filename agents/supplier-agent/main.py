from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
import uvicorn
import os
from datetime import datetime

from .database import Base, engine, get_db, Supplier, init_db
from .rag import generate_pestel_analysis
from shared.utils import register_agent

app = FastAPI(title="Supplier Risk Agent")

# Initialize DB on startup
@app.on_event("startup")
def on_startup():
    init_db()
    
    # Register with Orchestrator using Agent Card Skills
    skills = [
        {
            "id": "analyze-risk",
            "name": "Analyze Supplier Risk",
            "description": "Analyzes the PESTEL risk for a given supplier in a specific country.",
            "inputModes": ["text"],
            "outputModes": ["text", "json"],
            "parameters": {
                "type": "object",
                "properties": {
                    "supplier_name": {"type": "string", "description": "Name of the supplier"},
                    "country": {"type": "string", "description": "Country of the supplier"}
                },
                "required": ["supplier_name", "country"]
            }
        }
    ]
    register_agent("supplier-agent", 8001, skills)

@app.get("/.well-known/agent.json")
def get_agent_card():
    return {
        "name": "supplier-agent",
        "description": "Supplier Risk Analysis Agent",
        "url": "http://supplier-agent:8001",
        "version": "1.0.0",
        "skills": [
            {
                "id": "analyze-risk",
                "name": "Analyze Supplier Risk"
            }
        ]
    }


class RiskRequest(BaseModel):
    supplier_name: str
    country: str

class RiskResponse(BaseModel):
    supplier_name: str
    country: str
    risk_score: int
    summary: str
    pestel_data: dict

@app.post("/analyze-risk", response_model=RiskResponse)
def analyze_risk(request: RiskRequest, db: Session = Depends(get_db)):
    # Check cache
    supplier = db.query(Supplier).filter(
        Supplier.name == request.supplier_name, 
        Supplier.country == request.country
    ).first()
    
    if supplier and supplier.pestel_data:
        return RiskResponse(
            supplier_name=supplier.name,
            country=supplier.country,
            risk_score=supplier.risk_score,
            summary=supplier.pestel_data.get("summary", ""),
            pestel_data=supplier.pestel_data.get("pestel_breakdown", {})
        )
    
    # Generate new analysis
    analysis = generate_pestel_analysis(request.supplier_name, request.country)
    
    # Save to DB
    if not supplier:
        supplier = Supplier(
            name=request.supplier_name,
            country=request.country,
            risk_score=analysis.get("risk_score", 50),
            pestel_data=analysis
        )
        db.add(supplier)
    else:
        supplier.risk_score = analysis.get("risk_score", 50)
        supplier.pestel_data = analysis
        supplier.last_updated = datetime.utcnow()
        
    db.commit()
    db.refresh(supplier)
    
    return RiskResponse(
        supplier_name=supplier.name,
        country=supplier.country,
        risk_score=supplier.risk_score,
        summary=analysis.get("summary", ""),
        pestel_data=analysis.get("pestel_breakdown", {})
    )

@app.get("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8001)))
