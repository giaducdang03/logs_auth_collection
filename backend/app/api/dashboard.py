from fastapi import APIRouter, Depends, Query, HTTPException, status as http_status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional

from app.database import get_db
from app.schemas.dashboard_schemas import DashboardStatsResponse
from app.services.dashboard_service import DashboardService
from app.middleware import verify_jwt_token, security


router = APIRouter(prefix="/dashboard", tags=["dashboard"])


@router.get("/stats", response_model=DashboardStatsResponse)
def get_dashboard_stats(
    start_date: Optional[str] = Query(None, description="Start date (ISO format: YYYY-MM-DD)"),
    end_date: Optional[str] = Query(None, description="End date (ISO format: YYYY-MM-DD)"),
    granularity: str = Query("day", regex="^(day|week|month)$"),
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
        if start_date:
            start = datetime.fromisoformat(start_date)
        else:
            start, _ = DashboardService.get_default_date_range(days_back=7)
        
        if end_date:
            end = datetime.fromisoformat(end_date)
        else:
            _, end = DashboardService.get_default_date_range(days_back=7)
    except ValueError as e:
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid date format. Use ISO format (YYYY-MM-DD): {str(e)}",
        )
    
    # Validate date range
    if start >= end:
        raise HTTPException(
            status_code=http_status.HTTP_400_BAD_REQUEST,
            detail="start_date must be before end_date",
        )
    
    # Get stats from service
    stats = DashboardService.get_dashboard_stats(
        db=db,
        start_date=start,
        end_date=end,
        granularity=granularity,
        top_limit=10,
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
        if start_date:
            start = datetime.fromisoformat(start_date)
        else:
            start, _ = DashboardService.get_default_date_range(days_back=7)
        
        if end_date:
            end = datetime.fromisoformat(end_date)
        else:
            _, end = DashboardService.get_default_date_range(days_back=7)
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
        if start_date:
            start = datetime.fromisoformat(start_date)
        else:
            start, _ = DashboardService.get_default_date_range(days_back=7)
        
        if end_date:
            end = datetime.fromisoformat(end_date)
        else:
            _, end = DashboardService.get_default_date_range(days_back=7)
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
        if start_date:
            start = datetime.fromisoformat(start_date)
        else:
            start, _ = DashboardService.get_default_date_range(days_back=7)
        
        if end_date:
            end = datetime.fromisoformat(end_date)
        else:
            _, end = DashboardService.get_default_date_range(days_back=7)
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
