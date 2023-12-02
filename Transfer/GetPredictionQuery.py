from pydantic import BaseModel

from Transfer.CountryCodeDto import CountryCodeDto

_MINCOVERMULTIPLER = 2


class GetPredictionQuery(BaseModel):
    timeSeriesDictId: int
    timeSeriesDict: dict[str, float]
    predictionTicks: int
    countryCode: CountryCodeDto

    def IsValid(self) -> None:
        if not self.timeSeriesDict:
            raise Exception("Time series dictionary is empty")
        if not self.timeSeriesDictId:
            raise Exception("Time series dictionary id is empty")
        if self.predictionTicks >= len(self.timeSeriesDict) * _MINCOVERMULTIPLER:
            raise Exception(
                "Prediction ticks is too big. It should be less than 2 times bigger than time series dictionary length"
            )
        return None
