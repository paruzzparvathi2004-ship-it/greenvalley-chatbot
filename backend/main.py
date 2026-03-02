from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from .database.connection import init_db
from .routes.chat import router
from dotenv import load_dotenv
import os

load_dotenv()

app = FastAPI(title="GreenValley University Chatbot")

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
app.include_router(router, prefix="/api")
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

@app.on_event("startup")
async def startup():
    init_db()

@app.get("/")
async def root():
    return FileResponse("frontend/index.html")

@app.get("/{page}.html")
async def pages(page: str):
    return FileResponse(f"frontend/{page}.html")
