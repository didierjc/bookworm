import logging

from colorama import Fore, Style
from dotenv import load_dotenv
from functools import wraps
from logtail import LogtailHandler
from typing import Optional

from bookworm.config.settings import settings

# Load environment variables without exporting the variables explicitly by the export command
load_dotenv()

def log(log_name, message: Optional[str] = "", level: str = "info"):
    def decorator(func):
        # setup logger and handler
        logger = logging.getLogger(log_name)
        logger.setLevel(logging.DEBUG)

        handler = logging.StreamHandler()
        handler.setLevel(logging.DEBUG)

        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - METHOD >>> "
            + Fore.LIGHTCYAN_EX
            + "%(message)s"
            + Style.RESET_ALL
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
        ### [START] LogTail (lt) handler
        lt = LogtailHandler(source_token=settings.LOGTAIL_TOKEN)
        lt.setFormatter(formatter) # add formatter to lt
        logger.addHandler(lt) # add lt to logger

        @wraps(func)
        def wrapper(*args, **kwargs):
            # set name_override to func.__name__
            if message:
                logger.info(
                    Fore.LIGHTCYAN_EX + message + Style.RESET_ALL,
                    extra={"name_override": func.__name__},
                )

            output = func(*args, **kwargs)
            logger.info(f"{func.__name__} returned: {output}")

            return output

        return wrapper

    return decorator
