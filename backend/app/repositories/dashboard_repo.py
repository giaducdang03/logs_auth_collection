from sqlalchemy.orm import Session
from sqlalchemy import func, desc, and_, case
from datetime import datetime
from typing import List, Tuple, Literal
from app.models import SSHLog


class DashboardRepository:
    """Repository for dashboard analytics queries"""

    @staticmethod
    def get_user_frequency(
        db: Session,
        start_date: datetime,
        end_date: datetime,
        limit: int = 10,
    ) -> List[Tuple[str, int]]:
        """
        Get login frequency by username.
        
        Args:
            db: Database session
            start_date: Start date filter
            end_date: End date filter
            limit: Number of top users to return
            
        Returns:
            List of tuples (username, login_count)
        """
        query = (
            db.query(
                SSHLog.username,
                func.count(SSHLog.id).label("login_count"),
            )
            .filter(
                and_(
                    SSHLog.login_time >= start_date,
                    SSHLog.login_time < end_date,
                    SSHLog.status == "success",
                    SSHLog.username.isnot(None),
                )
            )
            .group_by(SSHLog.username)
            .order_by(desc("login_count"))
            .limit(limit)
        )
        return query.all()

    @staticmethod
    def get_top_ips(
        db: Session,
        start_date: datetime,
        end_date: datetime,
        limit: int = 10,
    ) -> List[Tuple[str, int, datetime]]:
        """
        Get top IP addresses by login attempts.
        
        Args:
            db: Database session
            start_date: Start date filter
            end_date: End date filter
            limit: Number of top IPs to return
            
        Returns:
            List of tuples (ip_address, attempt_count, last_attempt_at)
        """
        query = (
            db.query(
                SSHLog.ip_address,
                func.count(SSHLog.id).label("attempt_count"),
                func.max(SSHLog.login_time).label("last_attempt_at"),
            )
            .filter(
                and_(
                    SSHLog.login_time >= start_date,
                    SSHLog.login_time < end_date,
                    SSHLog.ip_address.isnot(None),
                )
            )
            .group_by(SSHLog.ip_address)
            .order_by(desc("attempt_count"), desc("last_attempt_at"))
            .limit(limit)
        )
        return query.all()

    @staticmethod
    def get_top_ips_by_status(
        db: Session,
        start_date: datetime,
        end_date: datetime,
        status: Literal["success", "failed"],
        limit: int = 10,
    ) -> List[Tuple[str, int, datetime]]:
        """
        Get top IP addresses by login attempts for a given status.

        Args:
            db: Database session
            start_date: Start date filter
            end_date: End date filter
            status: Login status ('success' or 'failed')
            limit: Number of top IPs to return

        Returns:
            List of tuples (ip_address, attempt_count, last_attempt_at)
        """
        query = (
            db.query(
                SSHLog.ip_address,
                func.count(SSHLog.id).label("attempt_count"),
                func.max(SSHLog.login_time).label("last_attempt_at"),
            )
            .filter(
                and_(
                    SSHLog.login_time >= start_date,
                    SSHLog.login_time < end_date,
                    SSHLog.ip_address.isnot(None),
                    SSHLog.status == status,
                )
            )
            .group_by(SSHLog.ip_address)
            .order_by(desc("attempt_count"), desc("last_attempt_at"))
            .limit(limit)
        )
        return query.all()

    @staticmethod
    def get_recent_activity(
        db: Session,
        start_date: datetime,
        end_date: datetime,
        limit: int = 5,
    ) -> List[Tuple[datetime, str, str, str, str]]:
        """
        Get most recent login activities.

        Returns:
            List of tuples (login_time, username, ip_address, status, auth_method)
        """
        query = (
            db.query(
                SSHLog.login_time,
                SSHLog.username,
                SSHLog.ip_address,
                SSHLog.status,
                SSHLog.auth_method,
            )
            .filter(
                and_(
                    SSHLog.login_time >= start_date,
                    SSHLog.login_time < end_date,
                )
            )
            .order_by(desc(SSHLog.login_time))
            .limit(limit)
        )
        return query.all()

    @staticmethod
    def get_timeline_data(
        db: Session,
        start_date: datetime,
        end_date: datetime,
        granularity: Literal["day", "week", "month"] = "day",
    ) -> List[Tuple[str, int, int]]:
        """
        Get timeline data for login attempts.
        
        Args:
            db: Database session
            start_date: Start date filter
            end_date: End date filter
            granularity: 'day', 'week', or 'month'
            
        Returns:
            List of tuples (time_bucket, success_count, failed_count)
        """
        # Determine the truncation level for date_trunc
        truncate_level = {
            "day": "day",
            "week": "week",
            "month": "month",
        }.get(granularity, "day")

        query = (
            db.query(
                func.date_trunc(truncate_level, SSHLog.login_time).label("time_bucket"),
                func.sum(
                    case(
                        (SSHLog.status == "success", 1),
                        else_=0
                    )
                ).label("success_count"),
                func.sum(
                    case(
                        (SSHLog.status == "failed", 1),
                        else_=0
                    )
                ).label("failed_count"),
            )
            .filter(
                and_(
                    SSHLog.login_time >= start_date,
                    SSHLog.login_time < end_date,
                )
            )
            .group_by("time_bucket")
            .order_by("time_bucket")
        )
        return query.all()

    @staticmethod
    def get_total_login_stats(
        db: Session,
        start_date: datetime,
        end_date: datetime,
    ) -> Tuple[int, int, int]:
        """
        Get total login statistics.
        
        Args:
            db: Database session
            start_date: Start date filter
            end_date: End date filter
            
        Returns:
            Tuple of (total_attempts, success_count, failed_count)
        """
        stats = db.query(
            func.count(SSHLog.id).label("total"),
            func.sum(
                case(
                    (SSHLog.status == "success", 1),
                    else_=0
                )
            ).label("success"),
            func.sum(
                case(
                    (SSHLog.status == "failed", 1),
                    else_=0
                )
            ).label("failed"),
        ).filter(
            and_(
                SSHLog.login_time >= start_date,
                SSHLog.login_time < end_date,
            )
        ).first()

        return (
            stats.total or 0,
            stats.success or 0,
            stats.failed or 0,
        )
