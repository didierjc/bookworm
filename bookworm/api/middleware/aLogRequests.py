from fastapi import HTTPException, Request

from colorama import Fore, Style
from datetime import datetime
from dotenv import load_dotenv
from logtail import LogtailHandler
from starlette.middleware.base import BaseHTTPMiddleware

from bookworm.config.settings import settings

import logging
import random
import string
import time

# Load environment variables without exporting the variables explicitly by the export command
load_dotenv()

# [START] default logger
logger = logging.getLogger(__name__)
logger.handlers = []
logger.setLevel(logging.DEBUG)  # Set minimal log level

# [START] default formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

### [START] LogTail (lt) handler
lt = LogtailHandler(source_token=settings.LOGTAIL_TOKEN)
lt.setFormatter(formatter)  # add formatter to lt
logger.addHandler(lt)  # add lt to logger

### [START] console handler (ch) and set level to debug
ch = logging.StreamHandler()
ch.setFormatter(formatter)  # add formatter to ch
logger.addHandler(ch)  # add ch to logger


class asyncLogRequests(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
    ):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        idem = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))

        logger.info(
            Fore.LIGHTGREEN_EX
            + f"rid={idem} >>> start: request = {request.url.path}"
            + Style.RESET_ALL
        )

        try:
            response = await call_next(request)

            # Getting the current date and time
            dt = datetime.now()
            # getting the timestamp
            ts = datetime.timestamp(dt)

            logger.info(
                Fore.LIGHTGREEN_EX
                + f"rid={idem} >>> end: status_code = {response.status_code}"
                + Style.RESET_ALL
            )
            logger.info(
                Fore.LIGHTGREEN_EX
                + f"rid={idem} >>> end: timer (ms) = {time.time() - start_time}"
                + Style.RESET_ALL
            )
            logger.info(
                Fore.LIGHTGREEN_EX
                + f"rid={idem} >>> Date and Time = {str(dt)}"
                + Style.RESET_ALL
            )
            logger.info(
                Fore.LIGHTGREEN_EX
                + f"rid={idem} >>> Timestamp = {str(ts)}"
                + Style.RESET_ALL
            )
            logger.info(
                Fore.LIGHTGREEN_EX
                + f"rid={idem} >>> environment = {settings.ENV_STATE}"
                + Style.RESET_ALL
            )
            logger.info(
                Fore.LIGHTGREEN_EX
                + f"rid={idem} >>> response = {response.__dict__}"
                + Style.RESET_ALL
            )

        except Exception as e:
            logger.error(
                Fore.LIGHTRED_EX + f"rid={idem} >>> error = {str(e)}" + Style.RESET_ALL
            )
            raise HTTPException(status_code=400, detail="Error")

        return response
