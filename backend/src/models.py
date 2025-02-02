from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from src.database import Base

class User(Base):
    """
    User model representing application users.
    
    Attributes:
        id (int): Unique user identifier
        username (str): Unique username for login
        email (str): User's email address
        hashed_password (str): Securely hashed user password
        is_active (bool): User account status
        is_superuser (bool): Admin/superuser status
        created_at (DateTime): User account creation timestamp
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<User {self.username}>"
