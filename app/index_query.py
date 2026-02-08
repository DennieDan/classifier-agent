import os

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
# Settings.llm = Ollama(model="llama3.3", request_timeout=200)
Settings.llm = Groq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))
Settings.embed_model = HuggingFaceEmbedding(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Connect to existing ChromaDB (no new documents)
print(CHROMA_PATH)
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
chroma_collection = chroma_client.get_collection(
    "web_collection"
)  # Use get_collection, not get_or_create

if chroma_collection.count() == 0:
    print(
        "Empty Response\n(The database has no documents. "
        "Run 'python app/index_server.py' first to populate it.)"
    )
else:
    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

    # Load index from existing vector store (no ingestion)
    index = VectorStoreIndex.from_vector_store(vector_store=vector_store)

    query_engine = index.as_query_engine()
    response = query_engine.query("What is title of the document?")
    print(response)
