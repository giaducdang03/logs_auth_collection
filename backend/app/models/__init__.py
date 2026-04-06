from sqlalchemy import Column, String, Boolean, DateTime, Text, Index, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID, INET
from datetime import datetime
import uuid

from app.database import Base


class User(Base):
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)


class SSHLog(Base):
    __tablename__ = "ssh_logs"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, nullable=True)
    ip_address = Column(INET, nullable=True)
    login_time = Column(DateTime(timezone=True), nullable=False)
    status = Column(String, nullable=False)  # 'success' or 'failed'
    auth_method = Column(String, nullable=True)  # 'password', 'publickey', 'unknown'
    ssh_key = Column(String, nullable=True)
    raw_log = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    
    __table_args__ = (
        Index("idx_ssh_logs_username", "username"),
        Index("idx_ssh_logs_ip", "ip_address"),
        Index("idx_ssh_logs_login_time", "login_time", postgresql_using="btree"),
        Index("idx_ssh_logs_status", "status"),
        Index("idx_ssh_logs_user_time", "username", "login_time"),
        Index("idx_ssh_logs_user_status_time", "username", "status", "login_time"),
        UniqueConstraint("username", "ip_address", "login_time", "status", name="uniq_ssh_log"),
    )


class UserSession(Base):
    __tablename__ = "user_sessions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    login_time = Column(DateTime(timezone=True), nullable=False, default=datetime.utcnow)
    ip_address = Column(INET, nullable=True)
    user_agent = Column(String, nullable=True)
