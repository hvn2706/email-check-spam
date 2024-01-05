import logging

from fastapi import APIRouter

from app.dto.spam_email_detection.email import SpamEmailDetectionRequest, SpamEmailDetectionResponse
from app.helper.base_response import DataResponse
from app.service.spam_email_detection import SpamEmailDetectionService

router = APIRouter()

_logger = logging.getLogger(__name__)


@router.post("/", response_model=DataResponse[SpamEmailDetectionResponse])
def detect_spam_email(request: SpamEmailDetectionRequest):
    data = SpamEmailDetectionService.detect_spam_email(request)
    return DataResponse().success_response(data=data)
