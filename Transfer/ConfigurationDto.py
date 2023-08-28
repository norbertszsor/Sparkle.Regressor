from pydantic import BaseModel


class _LoggerConfig(BaseModel):
    name: str | None
    level: str | None

class _DatabaseConfig(BaseModel):
    host: str | None
    name: str | None
    port: int | None
    user: str | None
    password: str | None

class Configuration(BaseModel):
    host: str | None
    port: int | None
    version: str | None
    env: str | None
    debug: bool | None
    logger: _LoggerConfig | None
    database: _DatabaseConfig | None