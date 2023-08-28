import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from logging import Logger

from fastapi import APIRouter, status
from fastapi.security import OAuth2PasswordRequestForm

from Services.ReggressorService import ReggressorService

from Providers.LoggerProvider import LoggerProvider

from Transfer.GetReggressorPredictionQuery import GetPredictionQuery
from Transfer.ServerResponseDto import ServerResponseDto

route = APIRouter()

_reggressorService: ReggressorService = ReggressorService()
_logger: Logger = LoggerProvider().GetLogger()


@route.post( "/reggressor/predict", status_code=status.HTTP_200_OK, response_model=ServerResponseDto, tags=["reggressor"])
async def GetPredictionQueryHandler(
    query: GetPredictionQuery,
) -> ServerResponseDto:
    try:
        query.IsValid()
        prediction = _reggressorService.GetReggresorPrediciton(query)
    except Exception as e:
        _logger.error(str(e))
        
        return ServerResponseDto(data=None, error=True, message=str(e))

    return ServerResponseDto(data=prediction, error=False, message=None)
