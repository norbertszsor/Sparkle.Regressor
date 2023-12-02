from pydantic import BaseModel

class PredictionDto(BaseModel):
    predictions: dict[str, float] | None
