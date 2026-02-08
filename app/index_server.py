import os

import chromadb
from dotenv import load_dotenv

load_dotenv()
from constants import CHROMA_PATH
from llama_index.core import Settings, SimpleDirectoryReader, VectorStoreIndex
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.groq import Groq
from llama_index.llms.ollama import Ollama
from llama_index.readers.web import BeautifulSoupWebReader
from llama_index.vector_stores.chroma import ChromaVectorStore

# Settings.llm = Ollama(model="llama3.3", request_timeout=200)
Settings.llm = Groq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))
Settings.embed_model = HuggingFaceEmbedding(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
print(CHROMA_PATH)
chroma_collection = chroma_client.get_or_create_collection("web_collection")
vector_store = ChromaVectorStore(chroma_collection=chroma_collection)

url = ["https://en.wikipedia.org/wiki/Artificial_intelligence"]
docs = BeautifulSoupWebReader().load_data(url)

# Path
# PDF_PATH = os.path.join(SCRIPT_DIR, "resources", "stcced2022.pdf")
# docs = SimpleDirectoryReader(input_files=[PDF_PATH]).load_data()

index = VectorStoreIndex.from_documents(docs, vector_store=vector_store)

query_engine = index.as_query_engine()
response = query_engine.query("Summarize the document into five bullet points")
print(response)
