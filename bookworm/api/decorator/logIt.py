import logging
import os

from colorama import Fore, Style

from dotenv import load_dotenv
from functools import wraps
from logtail import LogtailHandler
from typing import Optional

# Load environment variables without exporting the variables explicitly by the export command
load_dotenv()


def logIt(log_name, message: Optional[str] = "", level: Optional[str] = "debug"):
    def decorator(func):
        _level = logging.DEBUG

        if level.lower() == "info":
            _level = logging.INFO
        elif level.lower() == "warning":
            _level = logging.WARNING
        elif level.lower() == "error":
            _level = logging.ERROR

        # setup logger and handler
        logger = logging.getLogger(log_name)
        logger.setLevel(_level)

        handler = logging.StreamHandler()
        handler.setLevel(_level)

        formatter = logging.Formatter(
            f"LOGIT -- %(asctime)s - %(name)s - %(levelname)s - {log_name} >>> "
            + Fore.LIGHTCYAN_EX
            + "%(message)s"
            + Style.RESET_ALL
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        ### [START] LogTail (lt) handler
        lt = LogtailHandler(source_token=os.getenv("LOGTAIL_TOKEN"))
        lt.setFormatter(formatter)  # add formatter to lt
        logger.addHandler(lt)  # add lt to logger

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
