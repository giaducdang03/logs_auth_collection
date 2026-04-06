from sqlalchemy.orm import Session
from datetime import timedelta
from app.repositories import UserRepository
from app.utils.auth_utils import create_access_token


class AuthService:
    """Service for authentication operations"""
    
    @staticmethod
    def register_user(db: Session, username: str, password: str) -> dict:
        """Register a new user"""
        user = UserRepository.create_user(db, username, password)
        return {
            "id": str(user.id),
            "username": user.username,
            "is_active": user.is_active
        }
    
    @staticmethod
    def login_user(db: Session, username: str, password: str) -> dict:
        """Login user and return JWT token"""
        user = UserRepository.authenticate_user(db, username, password)
        
        access_token = create_access_token(
            data={"sub": user.username, "user_id": str(user.id)}
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer"
        }
