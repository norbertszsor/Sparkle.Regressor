from pydantic import BaseModel

class CountryCodeDto(BaseModel):
    code: str
    subdiv: str | None = None