from pydantic import BaseModel

class ServerResponseDto(BaseModel):
    data: object | None = None
    error: bool = False
    message: str | None = None
