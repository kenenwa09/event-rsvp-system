from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    PROJECT_NAME: str = "event"
    API_PREFIX: str = "/api"
    ENVIRONMENT: str = ""
    
    DATABASE_URL_ASYNC: str = ""
    DATABASE_URL_SYNC: str = ""
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )
    
settings = Settings()    