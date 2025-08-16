# backend/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.database import Base, engine
from backend.routes import keys, files, users, activity

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(title="Secure File System Backend")

# CORS configuration (allow frontend requests)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routes
app.include_router(keys.router, prefix="/keys", tags=["Keys"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(files.router, prefix="/files", tags=["Files"])
app.include_router(activity.router, prefix="/activity", tags=["Activity"])

# Health check endpoint
@app.get("/health")
def health():
    return {"status": "Abhinil is still hto"}
