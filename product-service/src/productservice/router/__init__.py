from fastapi import APIRouter
from .admin_router import router as admin_router

router = APIRouter(prefix="/v1")
router.include_router(admin_router)