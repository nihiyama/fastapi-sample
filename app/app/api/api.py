from fastapi import APIRouter

from app.api.api_v1 import auth, tenants, users

api_router = APIRouter()
api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(tenants.router, prefix="/tenants", tags=["tenants"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
