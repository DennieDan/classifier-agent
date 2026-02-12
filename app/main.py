from constants import get_llm
from fastapi import FastAPI, Request
from graph import AgentGraph
from langchain_core.messages import HumanMessage

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/health")
async def health():
    return {"status": "ok"}
