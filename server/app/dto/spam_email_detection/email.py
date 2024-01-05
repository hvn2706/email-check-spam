from pydantic import BaseModel


class SpamEmailDetectionRequest(BaseModel):
    subject: str
    content: str


class SpamEmailDetectionResponse(BaseModel):
    spam: bool
    cleanContent: str = None
    