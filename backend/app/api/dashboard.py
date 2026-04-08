from fastapi import APIRouter, Depends, Query, HTTPException, status as http_status
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional

from app.database import get_db
from app.schemas.dashboard_schemas import DashboardStatsResponse
from app.services.dashboard_service import DashboardService
from app.middleware import verify_jwt_token, security


router = APIRouter(prefix="/dashboard", tags=["dashboard"])


def _parse_datetime_param(date_value: str, is_end_date: bool = False) -> datetime:
    """
    Parse an ISO date/datetime string.

    If only a date is provided for end_date (YYYY-MM-DD), normalize to the
    start of the next day so repository filters can keep using [start, end).
    """
    parsed = datetime.fromisoformat(date_value)

    if is_end_date and len(date_value) == 10:
        return parsed + timedelta(days=1)

    return parsed


def _resolve_date_range(start_date: Optional[str], end_date: Optional[str]) -> tuple[datetime, datetime]:
    """Resolve query params into a validated datetime range."""
    default_start, default_end = DashboardService.get_default_date_range(days_back=7)

    start = _parse_datetime_param(start_date, is_end_date=False) if start_date else default_start
    end = _parse_datetime_param(end_date, is_end_date=True) if end_date else default_end

    if start >= end:
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail="start_date must be before end_date",
        )

    return start, end


@router.get("/stats", response_model=DashboardStatsResponse)
def get_dashboard_stats(
    start_date: Optional[str] = Query(None, description="Start date (ISO format: YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (ISO format: YYYY-MM-DD)"),
    granularity: str = Query("day", regex="^(day|week|month)$"),
    top_success_limit: int = Query(5, ge=1, le=100),
    top_failed_limit: int = Query(5, ge=1, le=100),
    db: Session = Depends(get_db),
    credentials=Depends(security),
):
    """
    Get dashboard statistics including:
    - User login frequency
    - Top IP addresses
    - Login timeline
    
    Query Parameters:
    - start_date: ISO format (YYYY-MM-DD), default is 7 days ago
    - end_date: ISO format (YYYY-MM-DD), default is now
    - granularity: 'day', 'week', or 'month' for timeline
    """
    
    # Verify JWT token
    verify_jwt_token(credentials)
    
    # Parse dates or use defaults
    try:
        start, end = _resolve_date_range(start_date, end_date)
    except ValueError as e:
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid date format. Use ISO format (YYYY-MM-DD): {str(e)}",
        )
    
    # Get stats from service
    stats = DashboardService.get_dashboard_stats(
        db=db,
        start_date=start,
        end_date=end,
        granularity=granularity,
        top_limit=10,
        top_success_limit=top_success_limit,
        top_failed_limit=top_failed_limit,
    )
    
    return DashboardStatsResponse(**stats)


@router.get("/user-frequency")
def get_user_frequency(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    credentials=Depends(security),
):
    """Get top users by login frequency"""
    verify_jwt_token(credentials)
    
    try:
        start, end = _resolve_date_range(start_date, end_date)
    except ValueError as e:
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid date format: {str(e)}",
        )
    
    stats = DashboardService.get_dashboard_stats(
        db=db,
        start_date=start,
        end_date=end,
        top_limit=limit,
    )
    
    return {"data": stats["user_frequency"]}


@router.get("/top-ips")
def get_top_ips(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    credentials=Depends(security),
):
    """Get top IP addresses by login attempts"""
    verify_jwt_token(credentials)
    
    try:
        start, end = _resolve_date_range(start_date, end_date)
    except ValueError as e:
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid date format: {str(e)}",
        )
    
    stats = DashboardService.get_dashboard_stats(
        db=db,
        start_date=start,
        end_date=end,
        top_limit=limit,
    )
    
    return {"data": stats["top_ips"]}


@router.get("/timeline")
def get_timeline(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    granularity: str = Query("day", regex="^(day|week|month)$"),
    db: Session = Depends(get_db),
    credentials=Depends(security),
):
    """Get login timeline data"""
    verify_jwt_token(credentials)
    
    try:
        start, end = _resolve_date_range(start_date, end_date)
    except ValueError as e:
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid date format: {str(e)}",
        )
    
    stats = DashboardService.get_dashboard_stats(
        db=db,
        start_date=start,
        end_date=end,
        granularity=granularity,
    )
    
    return {"data": stats["timeline"]}
