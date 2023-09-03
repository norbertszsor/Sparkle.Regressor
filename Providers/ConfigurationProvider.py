import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import json
from pydantic import parse_obj_as as ParseObjAs

from Transfer.ConfigurationDto import Configuration


class ConfigurationProvider:
    enviroment: str = os.environ.get("ENVIRONMENT", "development")

    def GetConfiguration(self) -> Configuration:
        with open(f"appsettings.{self.enviroment}.json", "r") as configFile:
            configJson = json.load(configFile)

        return ParseObjAs(Configuration, configJson)
