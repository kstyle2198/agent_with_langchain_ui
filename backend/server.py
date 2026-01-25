from fastapi import FastAPI
import uvicorn
from langserve import add_routes
from src.agent import agent

app = FastAPI()
add_routes(app, agent, path="/chat")


if __name__ == "__main__":
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=8000,
        reload=False
    )