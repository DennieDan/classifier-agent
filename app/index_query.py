import os
import time
from typing import Optional

import chromadb
import httpx
from constants import CHROMA_PATH, EMBED_MODEL
from dotenv import load_dotenv
from llama_index.core import Settings, VectorStoreIndex
from llama_index.core.response_synthesizers import ResponseMode
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.groq import Groq
from llama_index.llms.ollama import Ollama
from llama_index.vector_stores.chroma import ChromaVectorStore
from ollama import Client as OllamaClient

load_dotenv()


class IndexQuery:
    def __init__(self):
        self.ollama_timeout = httpx.Timeout(60.0, read=600.0)  # 10 min read timeout
        self.ollama_http = OllamaClient(
            host="http://localhost:11434", timeout=self.ollama_timeout
        )
        self.llm = Ollama(
            model="llama3.1:8b-instruct-q8_0",
            request_timeout=600.0,
            client=self.ollama_http,
        )
        self.embed_model = HuggingFaceEmbedding(model_name=EMBED_MODEL)
        # Use same embed model as index build so query embedding dimension matches collection (e.g. 384).
        Settings.embed_model = self.embed_model
        self.chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
        self.chroma_collection = self.chroma_client.get_collection("stcced_improved")

    def index_query(
        self, search_item: Optional[str] = None, query: Optional[str] = None
    ):
        if self.chroma_collection.count() == 0:
            return "Empty Response\n(The database has no documents. Run 'python app/index_server.py' first to populate it.)"
        else:
            vector_store = ChromaVectorStore(chroma_collection=self.chroma_collection)
            index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
            query_engine = index.as_query_engine()
            response = query_engine.query(
                query or f"What is the HS-Code of {search_item}?"
            )
            return str(response)


# Settings.llm = Groq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))


# print(
#     index_query(
#         query="""What are the General Interpretative Rules (GIR) in the STCCED 2022?
# Summarize each rule. If the rule have sub-part, summarize each part. There are 6 rules in total."""
#     )
# )
