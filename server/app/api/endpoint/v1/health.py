import logging
from fastapi import APIRouter

from app.helper.base_response import ResponseSchemaBase

router = APIRouter()
_logger = logging.getLogger(__name__)


@router.get("/", response_model=ResponseSchemaBase)
def health_check():
    return ResponseSchemaBase().success_response()
