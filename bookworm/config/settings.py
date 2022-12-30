from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    base = {
        "app_name": "BookWorm API",
        "admin_email": "didijc@booek.com",
        "items_per_user": 50,
        "debug": False,
        "testing": False,
    }

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class Production(Settings):
    super().base["environment"] = "Production"


class Development(Settings):
    super().base["environment"] = "Development"
    super().base["debug"] = True
    super().base["testing"] = True

    # Vault settings

    # Logtail settings
    logTail = {
        "source_id": "",
        "api_token": "",
    }

    # Sentry settings

    # Redis settings

    # Postgres settings

    # RabbitMQ settings

    # Celery settings

    # Papertrail settings


class QA(Settings):
    super().base["environment"] = "QA"


# this is the function that is used to get the settings based on the environment
@lru_cache()
def get_settings(self):
    __settings = self.Settings()

    try:
        if __settings["ENV_SETTINGS"].casefold().strip() == "production":
            return Production()
        elif __settings["ENV_SETTINGS"].casefold().strip() == "qa":
            return QA()
    except:
        return Development()

    return Development()


# Load settings
settings = get_settings()
