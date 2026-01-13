from fastapi import FastAPI
from app.api.v1.routes import leads

app = FastAPI(
    title="My FastAPI App",
    description="FastAPI backend",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"message": "FastAPI is running 🚀"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(leads.router, prefix="/api/v1/leads", tags=["Leads"])