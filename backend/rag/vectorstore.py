import chromadb
from sentence_transformers import SentenceTransformer
from .ingestion import load_pdfs, load_csvs, chunk_text
import os

model = SentenceTransformer("all-MiniLM-L6-v2")
chroma_client = chromadb.PersistentClient(path=os.getenv("CHROMA_DB_PATH", "./chroma_db"))
collection = chroma_client.get_or_create_collection("greenvalley")

def ingest_all():
    docs = load_pdfs() + load_csvs()
    all_chunks, ids, sources = [], [], []
    idx = 0
    for doc in docs:
        chunks = chunk_text(doc["content"])
        for c in chunks:
            all_chunks.append(c)
            ids.append(f"chunk_{idx}")
            sources.append(doc["source"])
            idx += 1
    if all_chunks:
        embeddings = model.encode(all_chunks).tolist()
        collection.upsert(documents=all_chunks, embeddings=embeddings, ids=ids,
                          metadatas=[{"source": s} for s in sources])
    return len(all_chunks)

def retrieve(query, top_k=4):
    embedding = model.encode([query]).tolist()
    results = collection.query(query_embeddings=embedding, n_results=top_k)
    return results["documents"][0] if results["documents"] else []
