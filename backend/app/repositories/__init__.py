from sqlalchemy.orm import Session
from app.models import User
from app.utils.auth_utils import hash_password, verify_password
from app.utils.exceptions import UserAlreadyExistsException, InvalidCredentialsException


class UserRepository:
    """Repository for user database operations"""
    
    @staticmethod
    def create_user(db: Session, username: str, password: str) -> User:
        """Create a new user"""
        # Check if user already exists
        existing_user = db.query(User).filter(User.username == username).first()
        if existing_user:
            raise UserAlreadyExistsException(f"User '{username}' already exists")
        
        password_hash = hash_password(password)
        user = User(username=username, password_hash=password_hash, is_active=True)
        db.add(user)
        db.commit()
        db.refresh(user)
        
        return user
    
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> User:
        """Get user by username"""
        return db.query(User).filter(User.username == username).first()
    
    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> User:
        """Authenticate user"""
        user = UserRepository.get_user_by_username(db, username)
        
        if not user or not verify_password(password, user.password_hash):
            raise InvalidCredentialsException("Invalid username or password")
        
        if not user.is_active:
            raise InvalidCredentialsException("User is inactive")
        
        return user
