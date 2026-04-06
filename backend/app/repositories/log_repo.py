from sqlalchemy.orm import Session
from sqlalchemy import desc, and_
from datetime import datetime
from typing import Optional, List, Tuple
from app.models import SSHLog


class LogRepository:
    """Repository for SSH log database operations"""
    
    @staticmethod
    def create_log(db: Session, log_data: dict) -> SSHLog:
        """Create a new SSH log entry"""
        ssh_log = SSHLog(**log_data)
        db.add(ssh_log)
        db.commit()
        db.refresh(ssh_log)
        return ssh_log
    
    @staticmethod
    def log_exists(db: Session, username: str, ip_address: str, login_time: datetime, status: str) -> bool:
        """Check if log entry already exists (prevent duplicates)"""
        return db.query(SSHLog).filter(
            and_(
                SSHLog.username == username,
                SSHLog.ip_address == ip_address,
                SSHLog.login_time == login_time,
                SSHLog.status == status
            )
        ).first() is not None
    
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
    ) -> Tuple[List[SSHLog], int]:
        """Query SSH logs with filters"""
        
        query = db.query(SSHLog)
        
        # Apply filters
        if username:
            query = query.filter(SSHLog.username.ilike(f"%{username}%"))
        
        if ip_address:
            query = query.filter(SSHLog.ip_address.cast(str).ilike(f"%{ip_address}%"))
        
        if status:
            query = query.filter(SSHLog.status == status)
        
        if from_time:
            query = query.filter(SSHLog.login_time >= from_time)
        
        if to_time:
            query = query.filter(SSHLog.login_time <= to_time)
        
        # Get total count before pagination
        total = query.count()
        
        # Apply sorting
        sort_column = getattr(SSHLog, sort_by, SSHLog.login_time)
        if sort_order.upper() == "DESC":
            query = query.order_by(desc(sort_column))
        else:
            query = query.order_by(sort_column)
        
        # Apply pagination
        offset = (page - 1) * page_size
        logs = query.offset(offset).limit(page_size).all()
        
        return logs, total
    
    @staticmethod
    def get_recent_offset(db: Session, limit: int = 1) -> Optional[datetime]:
        """Get the most recent log's login_time for tracking"""
        recent = db.query(SSHLog).order_by(desc(SSHLog.login_time)).limit(limit).first()
        return recent.login_time if recent else None
