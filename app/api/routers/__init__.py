# app/api/routers/__init__.py

from .auth import router as auth_router
from .user import router as user_router
from .auth import router as auth_router
from .user import router as user_router
from .company import router as company_router
from .model import router as model_router

__all__ = ["auth_router", "user_router", "auth_router", "user_router", "company_router", "model_router",]
