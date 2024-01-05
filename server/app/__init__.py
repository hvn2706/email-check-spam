from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
from starlette.middleware.cors import CORSMiddleware

from app.api.endpoint import api_router
from app.helper.exception_handler import CommonException, base_exception_handler, http_exception_handler, \
    validation_exception_handler, request_validation_exception_handler, fastapi_error_handler
from app.helper.middleware import LoggingMiddleware
from app.service.spam_email_detection import EmbeddingModel, SpamEmailDetectionModel


def create_app() -> FastAPI:
    app = FastAPI(
        title="Spam email detection",
    )
    
    app.middleware("http")(LoggingMiddleware())
    app.add_middleware(
        CORSMiddleware,
        allow_origins=['*'],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(prefix="/api", router=api_router)
    
    app.add_exception_handler(CommonException, base_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(ValidationError, validation_exception_handler)
    app.add_exception_handler(RequestValidationError, request_validation_exception_handler)
    app.add_exception_handler(Exception, fastapi_error_handler)
    
    EmbeddingModel.init_embedding_model()
    SpamEmailDetectionModel.init_spam_email_detection_model()
    
    return app
    