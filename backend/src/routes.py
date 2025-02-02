from datetime import timedelta, datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from src.database import get_db
from src.models import User
from src.schemas import (
    UserCreate, 
    UserResponse, 
    Token, 
    UserMetadataModel, 
    HealthCheckModel, 
    ApplicationMetadataModel, 
    AuthMetadataModel, 
    AppMetadataModel,
    SystemDiagnosticsModel,
    EnvironmentInfoModel
)
from src.security import (
    create_access_token, 
    get_password_hash, 
    verify_password, 
    get_current_user,
    get_current_active_user
)
from src.config import settings
import logging
import sys
import platform
import psutil

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('/app/backend/routes.log')
    ]
)
logger = logging.getLogger(__name__)

# Authentication Router
auth_router = APIRouter()

# User Router
user_router = APIRouter()

@auth_router.post("/register", response_model=UserResponse)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user in the system.
    
    Args:
        user (UserCreate): User registration details
        db (Session): Database session
    
    Returns:
        UserResponse: Created user details
    """
    # Use email as username if not provided
    username = user.username or user.email
    
    # Check if username or email already exists
    existing_user = db.query(User).filter(
        (User.username == username) | (User.email == user.email)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = User(
        username=username,
        email=user.email,
        hashed_password=hashed_password,
        is_active=True
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user

@auth_router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    OAuth2 compatible token login endpoint.
    
    Args:
        form_data (OAuth2PasswordRequestForm): Login credentials
        db (Session): Database session
    
    Returns:
        Token: Access token for authentication
    """
    try:
        logger.info(f"Login attempt for username/email: {form_data.username}")
        logger.info(f"Login attempt password length: {len(form_data.password)}")
        
        # Log all users in the database for debugging
        all_users = db.query(User).all()
        logger.info(f"Total users in database: {len(all_users)}")
        for u in all_users:
            logger.info(f"Existing user: username={u.username}, email={u.email}")
        
        # Try to find user by username or email
        user = (db.query(User)
                .filter(
                    (User.username == form_data.username) | 
                    (User.email == form_data.username)
                )
                .first())
        
        if not user:
            logger.warning(f"User not found: {form_data.username}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"User not found: {form_data.username}",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Log user details for debugging
        logger.info(f"User found: username={user.username}, email={user.email}")
        logger.info(f"Stored hashed password: {user.hashed_password}")
        
        # Verify password
        is_password_correct = verify_password(form_data.password, user.hashed_password)
        logger.info(f"Password verification result: {is_password_correct}")
        
        if not is_password_correct:
            logger.warning("Password verification failed")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        # Create access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"sub": user.username}, 
            expires_delta=access_token_expires
        )
        
        logger.info(f"Access token created for user: {user.username}")
        return {"access_token": access_token, "token_type": "bearer"}
    
    except HTTPException as he:
        # Re-raise HTTPException to preserve its details
        logger.error(f"HTTP Exception during login: {he.detail}")
        raise
    
    except Exception as e:
        logger.error(f"Unexpected error during login: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred during authentication: {str(e)}"
        )

@auth_router.get("/metadata", response_model=AppMetadataModel)
def get_app_metadata(
    current_user: User = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """
    Get comprehensive application metadata.
    
    Args:
        current_user (User): Currently authenticated user
        db (Session): Database session
    
    Returns:
        AppMetadataModel: Comprehensive application metadata
    """
    # System Diagnostics
    system_diagnostics = SystemDiagnosticsModel(
        python_version=platform.python_version(),
        os={
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine()
        },
        cpu={
            "cores": psutil.cpu_count(),
            "usage_percent": psutil.cpu_percent()
        },
        memory={
            "total": psutil.virtual_memory().total,
            "available": psutil.virtual_memory().available,
            "percent_used": psutil.virtual_memory().percent
        }
    )
    
    # Environment Info
    environment_info = EnvironmentInfoModel(
        debug=str(settings.DEBUG),
        cors_origins=settings.CORS_ORIGINS
    )
    
    # Health Check
    health_check = HealthCheckModel(
        status="healthy",
        application_name=settings.PROJECT_NAME,
        version="0.1.0",
        database_status="connected",
        timestamp=datetime.utcnow(),
        environment=environment_info,
        system_diagnostics=system_diagnostics
    )
    
    # User Metadata
    user_metadata = UserMetadataModel(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        is_active=current_user.is_active,
        is_superuser=current_user.is_superuser,
        last_login=datetime.utcnow()
    )
    
    # Authentication Metadata
    auth_metadata = AuthMetadataModel(
        token_type="bearer",
        access_token=create_access_token(
            data={"sub": current_user.username}, 
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        ),
        expires_at=datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        permissions=["read", "write"] if current_user.is_superuser else ["read"]
    )
    
    # Application Metadata
    app_metadata = ApplicationMetadataModel(
        name=settings.PROJECT_NAME,
        version="0.1.0",
        environment=settings.ENVIRONMENT,
        build_timestamp=settings.BUILD_TIMESTAMP,
        dependencies=settings.CORE_DEPENDENCIES
    )
    
    return AppMetadataModel(
        user=user_metadata,
        health=health_check,
        auth=auth_metadata,
        application=app_metadata
    )

@user_router.get("/me", response_model=UserResponse)
def read_users_me(current_user: User = Depends(get_current_active_user)):
    """
    Get the current authenticated user's details.
    
    Args:
        current_user (User): Authenticated user
    
    Returns:
        UserResponse: Current user details
    """
    return current_user

@user_router.get("/", response_model=List[UserResponse])
def read_users(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    Retrieve a list of users (admin-only endpoint).
    
    Args:
        skip (int): Number of users to skip
        limit (int): Maximum number of users to return
        db (Session): Database session
        current_user (User): Authenticated user
    
    Returns:
        List[UserResponse]: List of user details
    """
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to list users"
        )
    
    users = db.query(User).offset(skip).limit(limit).all()
    return users
