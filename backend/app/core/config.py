from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "BJJVault API"
    environment: str = "development"

    database_url: str = "sqlite:///./bjjvault.db"

    jwt_secret: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60 * 24 * 7

    google_client_id: str = ""
    google_client_secret: str = ""
    apple_client_id: str = ""
    apple_client_secret: str = ""

    oauth_redirect_base_url: str = "http://localhost:8000"
    frontend_base_url: str = "http://localhost:5173"

    applicationinsights_connection_string: str = ""

    class Config:
        env_file = ".env"


settings = Settings()
