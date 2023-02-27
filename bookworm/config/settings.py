from functools import lru_cache
from pydantic import BaseSettings, Field
from typing import Optional


class GlobalConfig(BaseSettings):
    """Global configurations."""

    # define global variables with the Field class
    ENV_STATE: str = Field(None, env="ENV_STATE")

    # environment specific variables do not need the Field class
    ADMIN: Optional[str] = None
    ADMIN_EMAIL: Optional[str] = None
    APP_NAME: Optional[str] = None
    DEBUG: Optional[bool] = None
    ITEMS_PER_USER: Optional[int] = None
    LOG_LEVEL: Optional[str] = None
    TEST: Optional[bool] = None
    VERSION: Optional[str] = None

    LOGTAIL_SOURCE_ID: Optional[str] = None
    LOGTAIL_TOKEN: Optional[str] = None
    LOGTAIL_URL: Optional[str] = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class Local(GlobalConfig):
    """Local configurations."""

    # Akeyless
    from bookworm.api.service.akeyless import Akeyless

    akeyless = Akeyless()

    # Postgres Config
    username: str = "postgres"
    password: str = "postgres"
    port: int = 5432
    host: str = "localhost"
    name: str = "bookworm"

    class Config:
        pass


class Development(GlobalConfig):
    """Development configurations."""

    class Config:
        pass


class Qa(GlobalConfig):
    """QA configurations."""

    class Config:
        pass


class Production(GlobalConfig):
    """Production configurations."""

    class Config:
        pass


class FactoryConfig:
    """Returns a config instance depending on the ENV_STATE variable."""

    def __init__(self, env_state: Optional[str]):
        self.env_state = env_state

    def __call__(self):
        if self.env_state == "local":
            return Local()  # type: ignore - suppress warning
        elif self.env_state == "development":
            return Development()  # type: ignore - suppress warning
        elif self.env_state == "qa":
            return Qa()  # type: ignore - suppress warning
        elif self.env_state == "production":
            return Production()  # type: ignore - suppress warning
        else:
            raise ValueError(">>> Invalid environment state.")


# # this is the function that is used to get the settings based on the environment
@lru_cache()
def get_settings():
    return FactoryConfig(GlobalConfig().ENV_STATE)()  # type: ignore - suppress warning


# Load settings
settings = get_settings()
