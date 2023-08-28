from pydantic import BaseModel

class ReggressorPredictionDto(BaseModel):
    predictions: dict[str, float] | None
