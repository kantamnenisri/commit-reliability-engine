fastapi
uvicorn
pydanticfrom fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import random

app = FastAPI(title="Commit Reliability Engine - ML Predictor")

# Define the expected data structure coming from the Feature Extractor
class CommitFeatures(BaseModel):
    commit_id: str
    files_changed: int
    lines_added: int
    calculated_complexity: float

@app.post("/predict")
async def predict_reliability_risk(features: CommitFeatures):
    """
    Ingests commit features and returns a reliability risk score.
    """
    # This simulates the inference step of your trained ML model
    base_risk = features.calculated_complexity * 2.5
    
    # Cap the maximum risk score at 100
    final_score = min(base_risk + random.uniform(0, 5), 100)
    
    # Determine the CI/CD pipeline action
    decision = "APPROVE"
    if final_score > 80:
        decision = "BLOCK"
    elif final_score > 50:
        decision = "WARN"
        
    return {
        "commit_id": features.commit_id,
        "risk_score": round(final_score, 2),
        "pipeline_action": decision
    }

@app.get("/ping")
async def ping():
    return "OK"

if __name__ == "__main__":
    # Runs the ML predictor service on port 8001
    uvicorn.run(app, host="0.0.0.0", port=8001)