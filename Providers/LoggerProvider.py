import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging

from Providers.ConfigurationProvider import ConfigurationProvider
from Transfer.ConfigurationDto import Configuration

_DEFAULTLOGGERNAME: str = "app"
_DEFAULTLOGGERLEVEL: int = logging.ERROR


class LoggerProvider:
    _configuration: Configuration = ConfigurationProvider().GetConfiguration()

    _logger: logging.Logger = None

    def __init__(self):
        self._logger = self._SetLogger()

    def GetLogger(self) -> logging.Logger:
        return self._logger

    def _SetLogger(self) -> logging.Logger:
        logger: logging.Logger = logging.getLogger(
            self._configuration.logger.name or _DEFAULTLOGGERNAME
        )

        logger.setLevel(
            logging.getLevelName(
                (self._configuration.logger.level or _DEFAULTLOGGERLEVEL).upper()
            )
        )

        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        )

        logger.addHandler(handler)
        return logger
