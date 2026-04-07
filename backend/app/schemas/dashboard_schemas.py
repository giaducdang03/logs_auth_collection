from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional
from typing_extensions import Literal


class TimelinePoint(BaseModel):
    time: str
    timestamp: str
    success_count: int
    failed_count: int
    total_count: int


class UserFrequencyItem(BaseModel):
    username: Optional[str]
    login_count: int


class TopIPItem(BaseModel):
    ip_address: Optional[str]
    attempt_count: int


class TotalStats(BaseModel):
    total_attempts: int
    success_count: int
    failed_count: int
    success_rate: float


class DateRange(BaseModel):
    start_date: str
    end_date: str


class DashboardStatsResponse(BaseModel):
    date_range: DateRange
    granularity: Literal["day", "week", "month"]
    total_stats: TotalStats
    user_frequency: List[UserFrequencyItem]
    top_ips: List[TopIPItem]
    timeline: List[TimelinePoint]


class DashboardQueryParams(BaseModel):
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    granularity: Literal["day", "week", "month"] = "day"
