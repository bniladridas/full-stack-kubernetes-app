from datetime import datetime, timedelta
from typing import Optional
import logging
import sys

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from src.config import settings
from src.database import get_db
from src.models import User

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('/app/backend/security.log')
    ]
)
logger = logging.getLogger(__name__)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against its hashed version."""
    logger.info(f"Attempting password verification")
    logger.info(f"Plain password length: {len(plain_password)}")
    logger.info(f"Stored hash: {hashed_password}")
    
    try:
        # Normalize the hash to handle different bcrypt representations
        normalized_hash = hashed_password.replace('$2y$', '$2b$')
        logger.info(f"Normalized hash: {normalized_hash}")
        
        # Verify the password
        result = pwd_context.verify(plain_password, normalized_hash)
        
        logger.info(f"Password verification result: {result}")
        return result
    
    except Exception as e:
        logger.error(f"Password verification error: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        
        # Additional debug information
        logger.error(f"Exception type: {type(e)}")
        logger.error(f"pwd_context schemes: {pwd_context.schemes}")
        logger.error(f"pwd_context default: {pwd_context.default}")
        
        return False

def get_password_hash(password: str) -> str:
    """Hash a password for storing."""
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token with optional custom expiration.
    
    Args:
        data (dict): Payload data to encode in the token
        expires_delta (Optional[timedelta]): Custom token expiration time
    
    Returns:
        str: Encoded JWT token
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.SECRET_KEY, 
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt

def get_current_user(
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(get_db)
) -> User:
    """
    Get the current authenticated user from a JWT token.
    
    Raises:
        HTTPException: If token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(
            token, 
            settings.SECRET_KEY, 
            algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise credentials_exception
    
    return user

def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Get the current active user.
    
    Raises:
        HTTPException: If user is not active
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=400, 
            detail="Inactive user"
        )
    return current_user
