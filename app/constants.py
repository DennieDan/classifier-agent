"""
Constants and shared configuration for the travel planner.
"""

import json
import os
from pathlib import Path

import httpx
from chromadb.api import EMBEDDING_KEY
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_ollama import ChatOllama
from ollama import Client as OllamaClient

load_dotenv()

# ============================================
# LLM CONFIGURATION
# ============================================

LLM_MODEL = "llama-3.3-70b-versatile"
# llama-3.1-8b-instant – Llama 3.1 8B
# llama-3.3-70b-versatile – Llama 3.1 70B
LLM_TEMPERATURE = 0
LLM_API_KEY = os.getenv("GROQ_API_KEY")

EMBED_MODEL = "BAAI/bge-small-en-v1.5"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
CHROMA_PATH = os.path.join(PROJECT_ROOT, "chroma_db")


def get_cloud_groq_llm(model: str = "llama-3.3-70b-versatile"):
    """Get configured LLM instance."""
    return ChatGroq(model=model, temperature=LLM_TEMPERATURE, groq_api_key=LLM_API_KEY)


def get_local_ollama_llm(model: str = "llama3.1:8b-instruct-q8_0"):
    """Get configured Ollama LLM instance."""
    ollama_llm = ChatOllama(
        model=model,
        temperature=0,
        client=OllamaClient(
            host="http://localhost:11434", timeout=httpx.Timeout(60.0, read=600.0)
        ),
        request_timeout=600,
    )
    return ollama_llm
