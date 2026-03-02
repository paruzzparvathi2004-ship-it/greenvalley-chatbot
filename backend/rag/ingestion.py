import fitz
import pandas as pd
import os

def load_pdfs(folder="documents"):
    docs = []
    for f in os.listdir(folder):
        if f.endswith(".pdf"):
            pdf = fitz.open(os.path.join(folder, f))
            text = ""
            for page in pdf:
                text += page.get_text()
            docs.append({"source": f, "content": text})
    return docs

def load_csvs(folder="documents"):
    docs = []
    for f in os.listdir(folder):
        if f.endswith(".csv") or f.endswith(".xlsx"):
            path = os.path.join(folder, f)
            df = pd.read_excel(path) if f.endswith(".xlsx") else pd.read_csv(path)
            text = df.to_string(index=False)
            docs.append({"source": f, "content": text})
    return docs

def chunk_text(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)
    return chunks
