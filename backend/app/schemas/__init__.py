from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime
from typing import Optional
from uuid import UUID


# Auth Schemas
class UserRegisterRequest(BaseModel):
    username: str
    password: str


class UserLoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


# Log Schemas
class SSHLogRecord(BaseModel):
    id: UUID
    username: Optional[str] = None
    ip_address: Optional[str] = None
    login_time: datetime
    status: str  # 'success' or 'failed'
    auth_method: Optional[str] = None  # 'password', 'publickey', 'unknown'
    ssh_key: Optional[str] = None
    created_at: datetime

    @field_validator("ip_address", mode="before")
    @classmethod
    def coerce_ip_address_to_string(cls, value):
        if value is None:
            return None
        return str(value)
    
    class Config:
        from_attributes = True


class LogListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    data: list[SSHLogRecord]


class LogQueryParams(BaseModel):
    page: int = 1
    page_size: int = 20
    username: Optional[str] = None
    ip: Optional[str] = None
    status: Optional[str] = None
    from_time: Optional[datetime] = None
    to_time: Optional[datetime] = None
    sort_by: str = "login_time"
    sort_order: str = "DESC"


# Error Response
class ErrorResponse(BaseModel):
    detail: str
    code: str
