from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.api.v1.routes import leads
from app.db.database import get_db

app = FastAPI(
    title="Lead Generation FastAPI Backend",
    description="FastAPI backend for lead generation",
    version="1.0.0",
)

# CORS configuration
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://lead-generation-web-clients.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
def root():
    return {"message": "FastAPI is running 🚀"}

# Basic health check
@app.get("/health")
def health_check():
    return {"status": "ok"}

# Database health check (real Postgres ping)
@app.get("/health/db")
def db_health(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"status": "database connected"}

# API routes
app.include_router(
    leads.router,
    prefix="/api/v1/leads",
    tags=["Leads"],
)
