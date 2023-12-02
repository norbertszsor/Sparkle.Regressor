import os
import sys
import uvicorn

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI

from Handlers.RegressorHandler import (
    route as regressorRoute,
)

from Providers.ConfigurationProvider import ConfigurationProvider, Configuration

_configuration: Configuration = ConfigurationProvider().GetConfiguration()

app = FastAPI(debug=_configuration.debug, version=_configuration.version)

app.include_router(regressorRoute, prefix="/api")

uvicorn.run(app, host=_configuration.host, port=_configuration.port)
