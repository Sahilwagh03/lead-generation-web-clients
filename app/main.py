from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # Add this import
from app.api.v1.routes import leads
from app.db.database import init_db

app = FastAPI(
    title="lead Generation FastAPI Backend",
    description="FastAPI backend",
    version="1.0.0"
)

# Add CORS middleware configuration
# Configure CORS
origins = [
    "http://localhost:3000",  # React frontend
    "http://127.0.0.1:3000",  # Alternative localhost
    "https://lead-generation-web-clients.vercel.app"
    # Add other origins as needed for production:
    # "https://yourfrontenddomain.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # List of allowed origins
    allow_credentials=True,  # Allow cookies/auth headers
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
    expose_headers=["*"],  # Expose all headers to the browser
)

@app.get("/")
def root():
    return {"message": "FastAPI is running 🚀"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.on_event("startup")
def startup():
    init_db()

app.include_router(leads.router, prefix="/api/v1/leads", tags=["Leads"])