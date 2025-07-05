from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    APP_NAME: str = "Inventory"
    SQLALCHEMY_DATABASE_URL: str = "postgresql://postgres:maitri@localhost/wordpress_auto"
    SECRET_KEY: str = "1f4cd5d9-504f-443e-9f85-181a1ed230d0"
    REFRESH_SECRET_KEY: str = "1f4cd5d9-504f-443e-9f85-181a1ed230d0"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # ✅ Add this to fix the Gemini error
    GEMINI_API_KEY: str

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"  # <- allow unused env vars (prevents future breaks)

settings = Settings()
