import os
from typing import Any, Dict, List, Optional

from pydantic_settings import BaseSettings
from pydantic import AnyUrl, field_validator, model_validator


class Settings(BaseSettings):
    # Hangi .env dosyasının yükleneceğini ENV_FILE ortam değişkeni ile kontrol edin
    ENV_FILE: str = ".env.dev"

    # Proje bilgileri
    PROJECT_NAME: str = "FastAPI Application"
    VERSION: str = "0.1.0"
    API_V1_STR: str = "/api/v1"
    DOCS_URL: Optional[str] = "/docs"
    REDOC_URL: Optional[str] = "/redoc"

    # CORS izin verilen origin listesi (virgülle ayrılmış .env değerinden list’e çevrilecek)
    BACKEND_CORS_ORIGINS: List[AnyUrl] = []

    # Uygulama portu ve debug modu
    PORT: int = 8000
    DEBUG: bool = False

    # PostgreSQL ayarları
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: Optional[str] = None

    MAX_MODEL_FILE_SIZE: int = 200 * 1024 * 1024
    MODEL_UPLOAD_DIR: str

    # JWT ayarları
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 gün

    class Config:
        case_sensitive = True
        env_file = os.getenv("ENV_FILE", ".env.dev")
        env_file_encoding = "utf-8"

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Any) -> List[AnyUrl]:
        """
        .env'den gelen virgülle ayrılmış string'i listeye dönüştür.
        """
        if isinstance(v, str):
            return [i.strip() for i in v.split(",") if i.strip()]
        return v  # eğer zaten liste geldiyse olduğu gibi bırak

    @model_validator(mode="before")
    @classmethod
    def assemble_db_connection(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        """
        Eğer SQLALCHEMY_DATABASE_URI doğrudan .env'de yoksa, 
        parçalı ayarlardan URI oluştur.
        """
        uri = values.get("SQLALCHEMY_DATABASE_URI")
        if uri:
            return values

        user = values.get("POSTGRES_USER")
        pw = values.get("POSTGRES_PASSWORD")
        server = values.get("POSTGRES_SERVER")
        db = values.get("POSTGRES_DB")
        values["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{user}:{pw}@{server}/{db}"
        return values


settings = Settings()
