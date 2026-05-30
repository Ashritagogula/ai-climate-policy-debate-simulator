from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from datetime import datetime
import json
import os

app = FastAPI()

class DebateRequest(BaseModel):
    topic: str
    rounds: int

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/policies/{country_code}")
def get_policy(country_code: str):
    path = f"data/policies/{country_code}_policy.json"

    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Policy not found")

    with open(path, "r") as f:
        return json.load(f)

@app.post("/debate/start")
def start_debate(request: DebateRequest):
    agents = ["USA", "EU", "China"]
    messages = []

    for round_num in range(1, request.rounds + 1):
        for agent in agents:
            messages.append({
                "round": round_num,
                "agent": agent,
                "message": f"{agent} discusses {request.topic}",
                "stance": "neutral",
                "timestamp": datetime.utcnow().isoformat()
            })

    return {"messages": messages}

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def home():
    return FileResponse("static/index.html")