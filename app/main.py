from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.api.v1.routes import internal, leads, notifications
from app.core.deps import verify_token
from app.db.database import get_db
from app.schemas.users import CreateUserRequest, TokenResponse , LoginRequest, UserOut
from app.db.models.users import User
from app.core.auth import create_access_token, hash_password, verify_password

app = FastAPI(
    title="Lead Generation FastAPI Backend",
    description="FastAPI backend for lead generation",
    version="1.0.0",
)

# CORS configuration
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://192.168.0.109:3000",
    "http://192.168.0.107:3000",
    "http://192.168.0.104:3000",
    "https://lead-gen-seven.vercel.app"
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

@app.post("/login", response_model=TokenResponse)
def login(data: LoginRequest, db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == data.email).first()

    if not user or not verify_password(data.password, user.password):
        raise HTTPException(401, "Invalid credentials")

    token = create_access_token({"user_id": user.id})
    
    return {
        "access_token": token,
        "id":user.id,
        "name": user.name,
        "email": user.email,
    }

@app.post("/create-user", response_model=UserOut)
def create_user(data: CreateUserRequest, db: Session = Depends(get_db)):

    existing = db.query(User).filter(User.email == data.email).first()
    if existing:
        raise HTTPException(400, "Email already exists")

    user = User(
        name=data.name,
        email=data.email,
        password=hash_password(data.password),
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

# API routes
app.include_router(
    leads.router,
    prefix="/api/v1/leads",
    tags=["Leads"],
    dependencies=[Depends(verify_token)]
)

app.include_router(notifications.router)
app.include_router(internal.router)
