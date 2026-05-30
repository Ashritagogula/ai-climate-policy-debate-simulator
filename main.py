from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from datetime import datetime
import json
import os

app = FastAPI(title="Climate Policy Debate Simulator")

class DebateRequest(BaseModel):
    topic: str
    rounds: int

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/policies/{country_code}")
def get_policy(country_code: str):
    file_path = f"data/policies/{country_code.lower()}_policy.json"

    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Policy not found")

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

@app.post("/debate/start")
def start_debate(request: DebateRequest):

    if request.rounds < 1 or request.rounds > 5:
        raise HTTPException(
            status_code=400,
            detail="Rounds must be between 1 and 5"
        )

    agents = ["USA", "EU", "China"]

    agent_messages = {
        "USA": "The USA supports renewable energy investments while balancing economic growth.",
        "EU": "The EU advocates strong emissions reductions and climate neutrality goals.",
        "China": "China supports international climate cooperation while maintaining development."
    }

    stances = {
        "USA": "supportive",
        "EU": "supportive",
        "China": "neutral"
    }

    messages = []

    for round_num in range(1, request.rounds + 1):
        for agent in agents:
            messages.append({
                "round": round_num,
                "agent": agent,
                "message": f"{agent_messages[agent]} Topic: {request.topic}",
                "stance": stances[agent],
                "timestamp": datetime.utcnow().isoformat()
            })

    return {"messages": messages}

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def home():
    return FileResponse("static/index.html")