import os
from dotenv import load_dotenv
from pydantic import BaseSettings, Field
from datetime import datetime
from typing import List

# Load environment variables
load_dotenv()

class Settings(BaseSettings):
    # Project Settings
    PROJECT_NAME: str = "Full-Stack Kubernetes App"
    PROJECT_DESCRIPTION: str = Field(
        default="Full-stack application with advanced metadata support", 
        description="Detailed description of the project"
    )
    
    # Environment configuration
    ENVIRONMENT: str = Field(
        default="development", 
        description="Current application environment"
    )
    
    # Build and version metadata
    BUILD_TIMESTAMP: datetime = Field(
        default_factory=datetime.utcnow, 
        description="Timestamp of the application build"
    )
    
    # Dependency tracking
    CORE_DEPENDENCIES: List[str] = Field(
        default=[
            "fastapi==0.95.1", 
            "sqlalchemy==1.4.46", 
            "pydantic==1.10.7"
        ],
        description="Core application dependencies"
    )
    
    # Database Configuration
    DB_HOST: str = os.getenv("DB_HOST", "postgres")
    DB_PORT: str = os.getenv("DB_PORT", "5432")
    DB_NAME: str = os.getenv("DB_NAME", "myappdb")
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "postgrespassword")
    
    # JWT Authentication
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # External Services
    KAFKA_BOOTSTRAP_SERVERS: str = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")
    
    # CORS Configuration
    CORS_ORIGINS: list = os.getenv("CORS_ORIGINS", 
        '["http://localhost:80", "http://localhost:8000", "http://frontend:80", "http://backend:8000"]'
    ).split(',')

    class Config:
        # Allows loading from .env file
        env_file = ".env"
        env_file_encoding = "utf-8"

# Create a singleton instance
settings = Settings()
