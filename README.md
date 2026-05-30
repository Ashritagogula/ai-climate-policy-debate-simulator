# AI Climate Policy Debate Simulator

FastAPI + Ollama based multi-agent climate policy debate simulator.

## Run

pip install -r requirements.txt

uvicorn main:app --reload

## Endpoints

GET /health

GET /policies/{country}

POST /debate/start