from fastapi.staticfiles import StaticFiles
import uvicorn
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.db.session import engine
from app.db.base import Base  # Tüm modeller buradan Base.metadata'ye eklenir
from app.api.routers import auth_router, user_router, company_router, model_router  # doğru router isimleri

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        version=settings.VERSION,
        docs_url=settings.DOCS_URL,
        redoc_url=settings.REDOC_URL,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
    )

    # CORS ayarları
    app.add_middleware(
        CORSMiddleware,
        # allow_origins=[str(o) for o in settings.BACKEND_CORS_ORIGINS],
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.mount(
        "/files",
        StaticFiles(directory=settings.MODEL_UPLOAD_DIR, html=False),
        name="files"
    )

    # Router’ları ekle (burada auth_router & user_router kullanıyoruz)
    app.include_router(auth_router, prefix=settings.API_V1_STR)
    app.include_router(user_router, prefix=settings.API_V1_STR)
    app.include_router(company_router, prefix=settings.API_V1_STR)
    app.include_router(model_router, prefix=settings.API_V1_STR)

    return app

# Burada create_app() ile 'app' oluşturulmalı, üstte değil
app = create_app()

@app.on_event("startup")
def on_startup():
    # Development amaçlı: tabloları otomatik oluşturur
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.PORT,
        reload=settings.DEBUG,
    )
