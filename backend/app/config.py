from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict
from functools import lru_cache


class Settings(BaseSettings):
    # Database
    db_host: str = "localhost"
    db_port: int = 5432
    db_user: str = "postgres"
    db_password: str = "postgres"
    db_name: str = "ubuntu_auth_log"
    
    # JWT
    jwt_secret: str = "your-secret-key-change-this-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24
    
    # Log Reader
    log_file_path: str = "/var/log/auth.log"
    log_offset_file_path: str = "/state/.log_offset"
    log_reader_interval_minutes: int = 10
    log_reader_initial_days: int = 2
    log_reader_large_file_mb: int = 20
    
    # API
    api_prefix: str = "/api"
    api_v1_prefix: str = "/api/v1"
    backend_root_path: str = ""
    
    # Environment
    environment: str = "development"
    debug: bool = True
    
    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=False,
        extra="ignore",
    )
    
    @property
    def database_url(self) -> str:
        return f"postgresql+pg8000://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
