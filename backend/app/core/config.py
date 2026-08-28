from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_name: str = "SIF Precursor Intelligence Backend"
    database_url: str = "sqlite:///./database.db"
    max_upload_mb: int = 250
    model_version: str = "baseline-v1"
    analysis_type: str = "baseline"
    cors_origins: str = "*"
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def cors_list(self) -> list[str]:
        return [x.strip() for x in self.cors_origins.split(",") if x.strip()]

settings = Settings()
