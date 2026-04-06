from fastapi import APIRouter, Depends, HTTPException, status as http_status, Query
from sqlalchemy.orm import Session
from datetime import datetime
from app.database import get_db
from app.schemas import LogListResponse
from app.services.log_service import LogService
from app.middleware import verify_jwt_token, security
from app.tasks import collect_logs

router = APIRouter(prefix="/logs", tags=["logs"])


@router.get("", response_model=LogListResponse)
def get_logs(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    username: str = Query(None),
    ip: str = Query(None),
    status: str = Query(None),
    from_time: datetime = Query(None),
    to_time: datetime = Query(None),
    sort_by: str = Query("login_time"),
    sort_order: str = Query("DESC"),
    db: Session = Depends(get_db),
    credentials = Depends(security)
):
    """Get SSH logs with filtering and pagination"""
    
    # Verify JWT token
    token_payload = verify_jwt_token(credentials)
    
    try:
        result = LogService.query_logs(
            db,
            page=page,
            page_size=page_size,
            username=username,
            ip_address=ip,
            status=status,
            from_time=from_time,
            to_time=to_time,
            sort_by=sort_by,
            sort_order=sort_order
        )
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve logs"
        )


@router.post("/reload")
def reload_logs_now(credentials=Depends(security)):
    """Trigger immediate log collection from auth log file."""
    verify_jwt_token(credentials)

    try:
        collect_logs()
        return {"detail": "Log reload triggered successfully"}
    except Exception as e:
        raise HTTPException(
            status_code=http_status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to reload logs"
        )
