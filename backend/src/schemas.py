from pydantic import BaseModel, EmailStr, constr, Field
from datetime import datetime
from typing import Optional, List, Dict, Any

class UserBase(BaseModel):
    """Base user model for shared attributes."""
    username: Optional[constr(min_length=3, max_length=50)] = None
    email: EmailStr

class UserCreate(UserBase):
    """Model for user registration."""
    password: constr(min_length=8)

class UserResponse(UserBase):
    """Model for user response, excluding sensitive information."""
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True

class Token(BaseModel):
    """JWT Token model."""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """Token payload data model."""
    username: Optional[str] = None

class SystemDiagnosticsModel(BaseModel):
    python_version: str
    os: Dict[str, str]
    cpu: Dict[str, Any]
    memory: Dict[str, float]

class EnvironmentInfoModel(BaseModel):
    debug: str
    cors_origins: List[str]

class HealthCheckModel(BaseModel):
    status: str = Field(..., description="Current system health status")
    application_name: str
    version: str
    database_status: str
    timestamp: datetime
    environment: EnvironmentInfoModel
    system_diagnostics: SystemDiagnosticsModel

class UserMetadataModel(BaseModel):
    id: Optional[int] = None
    username: str
    email: str
    is_active: bool
    is_superuser: bool
    last_login: Optional[datetime] = None
    created_at: Optional[datetime] = None

class ApplicationMetadataModel(BaseModel):
    name: str
    version: str
    environment: str
    build_timestamp: datetime
    dependencies: Optional[List[str]] = None

class AuthMetadataModel(BaseModel):
    token_type: str
    access_token: str
    expires_at: Optional[datetime] = None
    permissions: Optional[List[str]] = None

class AppMetadataModel(BaseModel):
    user: Optional[UserMetadataModel] = None
    health: Optional[HealthCheckModel] = None
    application: Optional[ApplicationMetadataModel] = None
    auth: Optional[AuthMetadataModel] = None
