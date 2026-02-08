"""
Constants and shared configuration for the travel planner.
"""

import json
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

# ============================================
# LLM CONFIGURATION
# ============================================

LLM_MODEL = "llama-3.3-70b-versatile"
# llama-3.1-8b-instant – Llama 3.1 8B
# llama-3.3-70b-versatile – Llama 3.1 70B
LLM_TEMPERATURE = 0
LLM_API_KEY = os.getenv("GROQ_API_KEY")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)
CHROMA_PATH = os.path.join(PROJECT_ROOT, "chroma_db")


def get_llm():
    """Get configured LLM instance."""
    return ChatGroq(
        model=LLM_MODEL, temperature=LLM_TEMPERATURE, groq_api_key=LLM_API_KEY
    )
