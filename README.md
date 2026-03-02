# GreenValley University Chatbot

An AI-powered RAG chatbot built for GreenValley University website.

## Tech Stack
- FastAPI + Python (Backend)
- PostgreSQL (Database)
- ChromaDB (Vector Store)
- Groq LLaMA3 (LLM)
- Sentence Transformers (Embeddings)
- Vanilla HTML/CSS/JS (Frontend)

## Setup Instructions

### 1. Clone the repository
git clone <your-repo-url>
cd greenvalley

### 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

### 3. Configure environment variables
cp .env.example .env
Add your GROQ_API_KEY in the .env file

### 4. Setup PostgreSQL
sudo service postgresql start
sudo -u postgres psql -c "CREATE USER chatbot_user WITH PASSWORD 'chatbot123';"
sudo -u postgres psql -c "CREATE DATABASE greenvalley_db OWNER chatbot_user;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE greenvalley_db TO chatbot_user;"

### 5. Ingest documents
python3 -c "
import sys, os
sys.path.insert(0, os.getcwd())
from dotenv import load_dotenv
load_dotenv()
from backend.rag.vectorstore import ingest_all
print(ingest_all(), 'chunks ingested')
"

### 6. Start the server
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000

### 7. Open in browser
http://localhost:8000
