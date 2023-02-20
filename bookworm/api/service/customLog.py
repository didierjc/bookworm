from colorama import Fore, Style

from dotenv import load_dotenv
from logtail import LogtailHandler
from typing import Optional

import logging

# Load environment variables without exporting the variables explicitly by the export command
load_dotenv()


class CustomLog:
    @classmethod
    def logThis(
        cls,
        log_name: str,
        message: Optional[str] = None,
        level: Optional[str] = "debug",
    ):
        from bookworm.config.settings import settings

        _level = logging.DEBUG

        if level.lower() == "info":
            _level = logging.INFO
        elif level.lower() == "warning":
            _level = logging.WARNING
        elif level.lower() == "error":
            _level = logging.ERROR

        # setup logger and handler
        logger = logging.getLogger(str(log_name))
        logger.setLevel(_level)

        handler = logging.StreamHandler()
        handler.setLevel(_level)

        formatter = logging.Formatter(
            f"%(asctime)s - %(name)s - %(levelname)s - {log_name} >>> "
            + Fore.LIGHTCYAN_EX
            + "%(message)s"
            + Style.RESET_ALL
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

        ### [START] LogTail (lt) handler
        lt = LogtailHandler(source_token=settings.LOGTAIL_TOKEN)
        lt.setFormatter(formatter)  # add formatter to lt
        logger.addHandler(lt)  # add lt to logger

        if level.lower() == "info":
            # INFO log message
            logger.info(
                Fore.LIGHTCYAN_EX + message + Style.RESET_ALL,
                extra={"name_override": __name__},
            )
        elif level.lower() == "warning":
            # WARNING log message
            logger.warning(
                Fore.LIGHTYELLOW_EX + message + Style.RESET_ALL,
                extra={"name_override": __name__},
            )
        elif level.lower() == "error":
            # ERROR log message
            logger.error(
                Fore.LIGHTRED_EX + message + Style.RESET_ALL,
                extra={"name_override": __name__},
            )
        else:
            # DEBUG log message
            logger.debug(
                Fore.LIGHTCYAN_EX + message + Style.RESET_ALL,
                extra={"name_override": __name__},
            )
