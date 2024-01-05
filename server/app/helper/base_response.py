from typing import TypeVar, Generic, Optional
from app.dto.base import CamelBaseModel

T = TypeVar("T")


class ResponseSchemaBase(CamelBaseModel):
    __abstract__ = True

    code: int = ""
    message: str = ""

    def success_response(self):
        self.code = 200
        self.message = 'Success'
        return self

    def fail_response(self, code: int, message: str):
        self.code = code
        self.message = message
        return self


class DataResponse(ResponseSchemaBase, Generic[T]):
    data: Optional[T] = None

    class Config:
        arbitrary_types_allowed = True

    def custom_response(self, code: int, message: str, data: T):
        self.code = code
        self.message = message
        self.data = data
        return self

    def success_response(self, data: Optional[T]):
        self.code = 200
        self.message = 'Success'
        self.data = data
        return self

    def fail_response(self, code: int, message: str, data: T = None):
        self.code = code
        self.message = message
        self.data = data
        return self
