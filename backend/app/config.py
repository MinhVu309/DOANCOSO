from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:///./nhatki.db"
    secret_key: str = "change-this-to-a-real-secret-key"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440  # 24 giờ
    module1_url: str = "http://localhost:8001"
    upload_dir: str = "uploads"
    max_upload_size: int = 5 * 1024 * 1024  # 5MB

    model_config = {"env_file": ".env"}


settings = Settings()
