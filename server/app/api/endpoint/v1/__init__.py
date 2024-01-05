from fastapi import APIRouter
from . import health, spam_email_detection

v1_router = APIRouter()

v1_router.include_router(health.router, prefix="/health")
v1_router.include_router(spam_email_detection.router, prefix="/email-spam-detection")
