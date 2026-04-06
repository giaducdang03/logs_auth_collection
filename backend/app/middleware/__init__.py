from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer
from app.utils.auth_utils import verify_token


security = HTTPBearer()


def verify_jwt_token(credentials) -> dict:
    """Verify JWT token from request"""
    
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing authentication credentials"
        )
    
    token = credentials.credentials
    
    try:
        payload = verify_token(token)
        return payload
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
