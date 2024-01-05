from fastapi import Request
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from app.helper.base_response import ResponseSchemaBase


class CommonException(Exception):
    http_code: int
    code: int
    message: str
    
    def __init__(self, http_code: int = None, code: int = None, message: str = None):
        self.http_code = http_code
        self.code = code
        self.message = message
    
    def __str__(self):
        return f'{self.http_code} - {self.code} - {self.message}'


class ValidateException(CommonException):
    
    def __init__(self, code: int = None, message: str = None):
        self.http_code = 400
        self.code = code if code else self.http_code
        self.message = message


class ExistedException(CommonException):
    
    def __init__(self, code: int = None, message: str = None):
        self.http_code = 409
        self.code = code if code else self.http_code
        self.message = message


async def base_exception_handler(request: Request, exc: CommonException):
    return JSONResponse(
        status_code=exc.http_code,
        content=jsonable_encoder(ResponseSchemaBase().custom_response(exc.code, exc.message))
    )


async def http_exception_handler(request: Request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content=jsonable_encoder(ResponseSchemaBase().custom_response(exc.status_code, exc.detail))
    )


async def validation_exception_handler(request: Request, exc):
    code, msg = request_get_message_validation(exc)
    return JSONResponse(
        status_code=400,
        content=jsonable_encoder(ResponseSchemaBase().custom_response(code, msg))
    )


async def request_validation_exception_handler(request: Request, exc):
    code, msg = request_get_message_validation(exc)
    return JSONResponse(
        status_code=400,
        content=jsonable_encoder(ResponseSchemaBase().custom_response(code, msg))
    )


async def fastapi_error_handler(request: Request, exc):
    msg = "Internal system error"
    return JSONResponse(
        status_code=500,
        content=jsonable_encoder(
            ResponseSchemaBase().custom_response(500, msg)
        )
    )


def request_get_message_validation(exc) -> (int, object):
    print(exc.errors())
    
    types = [error.get('type') for error in exc.errors()]
    messages = [error.get("loc")[len(error.get("loc")) - 1] for error in exc.errors()]
    limit_value = [error.get('ctx').get('limit_value') if error.get('ctx') else '' for error in exc.errors()]
    
    for err_type, msg, limit in zip(types, messages, limit_value):
        if err_type == "value_error.missing":
            return 402, f"Param {msg} is required"
        elif err_type == "value_error.any_str.min_length":
            return 412, f"{msg} must have at least {limit} characters"
        elif err_type == "value_error.any_str.max_length":
            return 411, f"{msg} must have at most {limit} characters"
    
    return 420, f"{messages[0]} is invalid"
