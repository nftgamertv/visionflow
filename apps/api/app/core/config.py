from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # App
    app_name: str = "VisionFlow API"
    debug: bool = False
    api_v1_prefix: str = "/api/v1"

    # Supabase
    supabase_url: str
    supabase_anon_key: str
    supabase_jwt_secret: str

    # Database
    database_url: str

    # Redis
    redis_url: str = "redis://localhost:6379"

    # S3/R2
    s3_endpoint_url: str
    s3_access_key_id: str
    s3_secret_access_key: str
    s3_bucket_name: str
    s3_region: str = "auto"

    # CORS
    cors_origins: list[str] = ["http://localhost:3000"]

    # Security
    jwt_algorithm: str = "HS256"
    jwt_audience: str = "authenticated"

    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    return Settings()
