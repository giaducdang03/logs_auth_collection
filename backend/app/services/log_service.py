from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional, List
from app.repositories.log_repo import LogRepository
from app.schemas import SSHLogRecord, LogListResponse


class LogService:
    """Service for SSH log operations"""
    
    @staticmethod
    def create_log(db: Session, log_data: dict) -> SSHLogRecord:
        """Create a new SSH log entry"""
        # Check for duplicates
        if LogRepository.log_exists(
            db,
            log_data.get("username"),
            log_data.get("ip_address"),
            log_data.get("login_time"),
            log_data.get("status")
        ):
            return None  # Skip duplicate
        
        ssh_log = LogRepository.create_log(db, log_data)
        return SSHLogRecord.model_validate(ssh_log)
    
    @staticmethod
    def query_logs(
        db: Session,
        page: int = 1,
        page_size: int = 20,
        username: Optional[str] = None,
        ip_address: Optional[str] = None,
        status: Optional[str] = None,
        from_time: Optional[datetime] = None,
        to_time: Optional[datetime] = None,
        sort_by: str = "login_time",
        sort_order: str = "DESC"
    ) -> LogListResponse:
        """Query SSH logs with filters and return paginated response"""
        
        logs, total = LogRepository.query_logs(
            db,
            page=page,
            page_size=page_size,
            username=username,
            ip_address=ip_address,
            status=status,
            from_time=from_time,
            to_time=to_time,
            sort_by=sort_by,
            sort_order=sort_order
        )
        
        log_records = [SSHLogRecord.model_validate(log) for log in logs]
        
        return LogListResponse(
            total=total,
            page=page,
            page_size=page_size,
            data=log_records
        )
