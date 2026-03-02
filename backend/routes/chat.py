from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from ..database.connection import get_db, ChatQuery, Application
from ..services.chat_service import get_chat_response, extract_app_id
from ..rag.vectorstore import retrieve
import uuid

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    session_id: str = None

@router.post("/chat")
async def chat(req: ChatRequest, db: Session = Depends(get_db)):
    session_id = req.session_id or str(uuid.uuid4())
    message = req.message

    app_id = extract_app_id(message)
    if app_id:
        app = db.query(Application).filter(Application.id == app_id).first()
        if app:
            response = f"Application **{app.id}** for {app.applicant_name} ({app.program}) is currently **{app.status}**."
        else:
            response = f"No application found with ID {app_id}. Please check and try again."
    else:
        chunks = retrieve(message)
        if not chunks:
            response = "I'm sorry, I couldn't find relevant information. Please contact admissions@greenvalley.edu."
        else:
            response = get_chat_response(message, chunks)

    db.add(ChatQuery(session_id=session_id, user_message=message, bot_response=response))
    db.commit()

    return {"response": response, "session_id": session_id}

@router.post("/ingest")
async def ingest_documents():
    from ..rag.vectorstore import ingest_all
    count = ingest_all()
    return {"message": f"Ingested {count} chunks successfully"}

@router.get("/application/{app_id}")
async def get_application(app_id: str, db: Session = Depends(get_db)):
    app = db.query(Application).filter(Application.id == app_id.upper()).first()
    if not app:
        return {"error": "Application not found"}
    return {"id": app.id, "name": app.applicant_name, "program": app.program, "status": app.status}
