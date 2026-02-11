import os
import time

import chromadb
from dotenv import load_dotenv

load_dotenv()
from constants import CHROMA_PATH, SCRIPT_DIR
from llama_index.core import (
    Settings,
    SimpleDirectoryReader,
    StorageContext,
    VectorStoreIndex,
)
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.groq import Groq
from llama_index.llms.ollama import Ollama
from llama_index.readers.web import BeautifulSoupWebReader
from llama_index.vector_stores.chroma import ChromaVectorStore

Settings.llm = Ollama(model="llama3.1:8b-instruct-q8_0", request_timeout=1000)
# Settings.llm = Groq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))
# Settings.embed_model = HuggingFaceEmbedding(
#     model_name="sentence-transformers/all-MiniLM-L6-v2"
# )
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")

# Ensure a whole page fit in one block
Settings.node_parser = SentenceSplitter(chunk_size=1024, chunk_overlap=200)

chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
print(CHROMA_PATH)
# chroma_collection = chroma_client.get_or_create_collection("stcced_collection")
chroma_collection = chroma_client.get_or_create_collection("stcced_final")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

# StorageContext must include the vector_store for persistence to ChromaDB.
# Passing vector_store= to from_documents() is ignored; it uses in-memory store by default.
storage_context = StorageContext.from_defaults(vector_store=vector_store)

# url = ["https://en.wikipedia.org/wiki/Artificial_intelligence"]
# docs = BeautifulSoupWebReader().load_data(url)

# Path
PDF_PATH = os.path.join(SCRIPT_DIR, "resources", "stcced2022.pdf")
docs = SimpleDirectoryReader(input_files=[PDF_PATH]).load_data()

print("Building Index (this may take time)...")
start_time = time.time()
index = VectorStoreIndex.from_documents(docs, storage_context=storage_context)
end_time = time.time()
print(f"Index built in {end_time - start_time:.2f} seconds")

# similarity_top_k: return the top k results, not just the best match
query_engine = index.as_query_engine(similarity_top_k=10)
response = query_engine.query("What are ALL the General Interpretative Rules (GIR)?")
print("\n--- Response ---")
print(response)
