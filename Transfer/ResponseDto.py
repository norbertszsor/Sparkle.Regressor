from pydantic import BaseModel

class ResponseDto(BaseModel):
    data: object | None = None
    error: bool = False
    message: str | None = None
