import os

import chromadb
from constants import CHROMA_PATH
from dotenv import load_dotenv
from llama_index.core import Settings, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.groq import Groq
from llama_index.vector_stores.chroma import ChromaVectorStore

load_dotenv()

# --- 1. Setup Models (Same as before) ---
Settings.llm = Groq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))
Settings.embed_model = HuggingFaceEmbedding(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# --- 2. Connect to the Existing Database ---
# Ensure CHROMA_PATH is the same path used in your creation script
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)

# Get the collection you already created
chroma_collection = chroma_client.get_or_create_collection("web_collection")

# Connect the store
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

# --- 3. Load the Index from the Vector Store ---
# CRITICAL CHANGE: We use .from_vector_store instead of .from_documents
# This tells LlamaIndex: "The embeddings are already there, just wrap them."
index = VectorStoreIndex.from_vector_store(
    vector_store=vector_store,
)

# --- 4. Query ---
query_engine = index.as_query_engine()
response = query_engine.query("Summarize the document into five bullet points")
print(response)
