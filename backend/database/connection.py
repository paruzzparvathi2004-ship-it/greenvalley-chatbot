from sqlalchemy import create_engine, Column, String, Text, DateTime, Integer
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

class Application(Base):
    __tablename__ = "applications"
    id = Column(String, primary_key=True)
    applicant_name = Column(String)
    program = Column(String)
    status = Column(String)
    updated_at = Column(DateTime, default=datetime.utcnow)

class ChatQuery(Base):
    __tablename__ = "chat_queries"
    id = Column(Integer, primary_key=True, autoincrement=True)
    session_id = Column(String)
    user_message = Column(Text)
    bot_response = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    if not db.query(Application).first():
        samples = [
            Application(id="APP001", applicant_name="Rahul Sharma", program="B.Tech CSE", status="Approved"),
            Application(id="APP002", applicant_name="Priya Singh", program="MBA", status="Pending"),
            Application(id="APP003", applicant_name="Amit Kumar", program="B.Sc Physics", status="Rejected"),
            Application(id="APP004", applicant_name="Sneha Patel", program="M.Tech AI", status="Approved"),
        ]
        db.add_all(samples)
        db.commit()
    db.close()
