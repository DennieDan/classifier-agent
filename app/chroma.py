import chromadb

from constants import CHROMA_PATH

print(CHROMA_PATH)
chroma_client = chromadb.PersistentClient(path=CHROMA_PATH)
collections = chroma_client.list_collections()

for c in collections:
    print(c.name)
    print(f"Number of documents: {c.count()}")  # e.g. "rag_collection"
    print(f"Collection metadata: {c.metadata}")  # e.g. "rag_collection"
