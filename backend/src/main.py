import uvicorn
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator
import os
import platform
import psutil
from datetime import datetime
from sqlalchemy import text
from sqlalchemy.orm import Session
import logging
import sys

from src.database import engine, Base, get_db
from src.routes import auth_router, user_router
from src.config import Settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),  # Log to console
        logging.FileHandler('/app/backend/app.log')  # Log to file
    ]
)

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
settings = Settings()
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version="0.1.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
app.include_router(user_router, prefix="/api/users", tags=["Users"])

# Prometheus Metrics
Instrumentator().instrument(app).expose(app)

@app.get("/health")
async def health_check(db: Session = Depends(get_db)):
    try:
        # Attempt to execute a simple database query
        db.execute(text("SELECT 1"))
        database_status = "connected"
    except Exception as e:
        database_status = f"disconnected: {str(e)}"

    return {
        "status": "healthy",
        "application_name": settings.PROJECT_NAME,
        "version": "0.1.0",
        "database_status": database_status,
        "timestamp": datetime.utcnow().isoformat(),
        "environment": {
            "debug": os.getenv("DEBUG", "false"),
            "cors_origins": settings.CORS_ORIGINS
        },
        "system_diagnostics": {
            "python_version": platform.python_version(),
            "os": {
                "system": platform.system(),
                "release": platform.release(),
                "machine": platform.machine()
            },
            "cpu": {
                "cores": psutil.cpu_count(),
                "usage_percent": psutil.cpu_percent()
            },
            "memory": {
                "total": psutil.virtual_memory().total / (1024 * 1024),
                "available": psutil.virtual_memory().available / (1024 * 1024),
                "percent_used": psutil.virtual_memory().percent
            }
        }
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True
    )
