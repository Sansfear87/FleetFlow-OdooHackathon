# core/config.py

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL:                str
    SECRET_KEY:                  str
    ALGORITHM:                   str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    FRONTEND_URL:                str = "http://localhost:3000"
    ENVIRONMENT:                 str = "development"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
