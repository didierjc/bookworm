from fastapi import HTTPException, Request

from colorama import Fore, Style
from logtail import LogtailHandler
from starlette.middleware.base import BaseHTTPMiddleware

from config.settings import Settings

import logging
import random
import string

# [START] default logger
logger = logging.getLogger(__name__)
logger.handlers = []
logger.setLevel(logging.DEBUG) # Set minimal log level

# [START] default formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

### [START] LogTail (lt) handler
lt = LogtailHandler(source_token=Settings.LOGTAIL_TOKEN, host=Settings.LOGTAIL_HOST)
lt.setFormatter(formatter) # add formatter to lt
logger.addHandler(lt) # add lt to logger

### [START] console handler (ch) and set level to debug
ch = logging.StreamHandler()
ch.setFormatter(formatter) # add formatter to ch
logger.addHandler(ch) # add ch to logger


class asyncLogRequests(BaseHTTPMiddleware):
    def __init__(
        self,
        app,
    ):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        idem = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))

        logger.info(
            Fore.LIGHTGREEN_EX
            + f"rid={idem} >>> start: request = {request.url.path}"
            + Style.RESET_ALL
        )

        try:
            response = await call_next(request)
            logger.info(
                Fore.LIGHTGREEN_EX
                + f"rid={idem} >>> end: status_code = {response.status_code}"
                + Style.RESET_ALL
            )

        except Exception as e:
            logger.error(
                Fore.LIGHTRED_EX + f"rid={idem} >>> error = {str(e)}" + Style.RESET_ALL
            )
            raise HTTPException(status_code=400, detail="Error")

        return response
