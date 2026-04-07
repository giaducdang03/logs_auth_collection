from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import List, Dict, Any, Literal
from app.repositories.dashboard_repo import DashboardRepository


class DashboardService:
    """Service layer for dashboard analytics"""

    @staticmethod
    def get_dashboard_stats(
        db: Session,
        start_date: datetime,
        end_date: datetime,
        granularity: Literal["day", "week", "month"] = "day",
        top_limit: int = 10,
    ) -> Dict[str, Any]:
        """
        Get complete dashboard statistics.
        
        Args:
            db: Database session
            start_date: Start date filter
            end_date: End date filter
            granularity: 'day', 'week', or 'month' for timeline
            top_limit: Number of top users/IPs to return
            
        Returns:
            Dictionary containing all dashboard stats
        """
        # Fetch all data from repository
        user_frequency = DashboardRepository.get_user_frequency(
            db, start_date, end_date, limit=top_limit
        )
        top_ips = DashboardRepository.get_top_ips(
            db, start_date, end_date, limit=top_limit
        )
        timeline_data = DashboardRepository.get_timeline_data(
            db, start_date, end_date, granularity
        )
        total_stats = DashboardRepository.get_total_login_stats(
            db, start_date, end_date
        )

        # Format the response
        return {
            "date_range": {
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
            },
            "granularity": granularity,
            "total_stats": {
                "total_attempts": total_stats[0],
                "success_count": total_stats[1],
                "failed_count": total_stats[2],
                "success_rate": (
                    round((total_stats[1] / total_stats[0]) * 100, 2)
                    if total_stats[0] > 0
                    else 0
                ),
            },
            "user_frequency": [
                {
                    "username": username,
                    "login_count": count,
                }
                for username, count in user_frequency
            ],
            "top_ips": [
                {
                    "ip_address": str(ip) if ip else None,
                    "attempt_count": count,
                }
                for ip, count in top_ips
            ],
            "timeline": DashboardService._format_timeline(
                timeline_data, granularity
            ),
        }

    @staticmethod
    def _format_timeline(
        timeline_data: List[tuple],
        granularity: Literal["day", "week", "month"],
    ) -> List[Dict[str, Any]]:
        """
        Format timeline data for frontend consumption.
        
        Args:
            timeline_data: Raw timeline data from repository
            granularity: 'day', 'week', or 'month'
            
        Returns:
            Formatted list of timeline points
        """
        formatted = []
        for time_bucket, success_count, failed_count in timeline_data:
            if time_bucket is None:
                continue

            # Format the time bucket based on granularity
            if granularity == "day":
                time_label = time_bucket.strftime("%Y-%m-%d")
            elif granularity == "week":
                # Format as "2025-01 (Week 1)" or similar
                week_num = time_bucket.isocalendar()[1]
                year = time_bucket.year
                time_label = f"{year}-W{week_num:02d}"
            else:  # month
                time_label = time_bucket.strftime("%Y-%m")

            formatted.append(
                {
                    "time": time_label,
                    "timestamp": time_bucket.isoformat(),
                    "success_count": success_count or 0,
                    "failed_count": failed_count or 0,
                    "total_count": (success_count or 0) + (failed_count or 0),
                }
            )

        return formatted

    @staticmethod
    def get_default_date_range(
        days_back: int = 7,
    ) -> tuple[datetime, datetime]:
        """
        Get default date range (last N days).
        
        Args:
            days_back: Number of days to go back
            
        Returns:
            Tuple of (start_date, end_date)
        """
        end_date = datetime.utcnow()
        start_date = end_date - timedelta(days=days_back)
        return start_date, end_date
