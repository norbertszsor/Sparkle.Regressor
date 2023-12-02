import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import APIRouter, status
from fastapi.security import OAuth2PasswordRequestForm

from Services.RegressorService import ReggressorService

from Transfer.GetPredictionQuery import GetPredictionQuery
from Transfer.ResponseDto import ResponseDto

route = APIRouter()

_reggressorService: ReggressorService = ReggressorService()


@route.post(
    "/regressor/predict",
    status_code=status.HTTP_200_OK,
    response_model=ResponseDto,
    tags=["regressor"],
)
async def GetPredictionQueryHandlerAsync(
    query: GetPredictionQuery,
) -> ResponseDto:
    try:
        query.IsValid()
        prediction = _reggressorService.GetRegresorPrediciton(query)
    except Exception as e:
        return ResponseDto(data=None, error=True, message=str(e))

    return ResponseDto(data=prediction, error=False, message=None)
