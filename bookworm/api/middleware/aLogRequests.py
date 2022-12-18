from fastapi import HTTPException, Request
from colorama import Fore, Style
from starlette.middleware.base import BaseHTTPMiddleware

import logging
import random
import string

# create logger
logger = logging.getLogger("booek")
logger.setLevel(logging.DEBUG)

# create console handler (ch) and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)


class asyncLogRequests(BaseHTTPMiddleware):
    def __init__(self, app,):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        idem = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))

        logger.info(Fore.LIGHTGREEN_EX + f"rid={idem} >>> start: request = {request.url.path}" + Style.RESET_ALL)

        try:
            response = await call_next(request)
            logger.info(Fore.LIGHTGREEN_EX + f"rid={idem} >>> end: status_code = {response.status_code}" + Style.RESET_ALL)

        except Exception as e:
            logger.error(Fore.LIGHTRED_EX + f"rid={idem} >>> error = {str(e)}" + Style.RESET_ALL)
            raise HTTPException(status_code=400, detail="Error")

        return response
