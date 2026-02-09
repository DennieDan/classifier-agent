import os
import time

import chromadb
from constants import CHROMA_PATH
from dotenv import load_dotenv
from llama_index.core import Settings, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.groq import Groq
from llama_index.llms.ollama import Ollama
from llama_index.vector_stores.chroma import ChromaVectorStore

load_dotenv()

# Same LLM and embed model as index_server.py
Settings.llm = Ollama(model="llama3.1:8b-instruct-q8_0", request_timeout=1000)
# Settings.llm = Groq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))
Settings.embed_model = HuggingFaceEmbedding(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


def index_query(search_item: str):
    # Same LLM and embed model as index_server.py
    start_time = time.time()
    Settings.llm = Ollama(model="llama3.1:8b-instruct-q8_0", request_timeout=1000)
    Settings.embed_model = HuggingFaceEmbedding(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Connect to existing ChromaDB (no new documents)
    print(CHROMA_PATH)
    chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
    chroma_collection = chroma_client.get_collection(
        "stcced_collection"
    )  # Use get_collection, not get_or_create

    if chroma_collection.count() == 0:
        msg = (
            "Empty Response\n(The database has no documents. "
            "Run 'python app/index_server.py' first to populate it.)"
        )
        print(msg)
        return msg
    else:
        vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

        # Load index from existing vector store (no ingestion)
        index = VectorStoreIndex.from_vector_store(vector_store=vector_store)

        query_engine = index.as_query_engine()
        response = query_engine.query(f"What is the HS-Code of {search_item}?")
        print(response)
        end_time = time.time()
        print(f"Time taken: {end_time - start_time} seconds")
        return str(response)
