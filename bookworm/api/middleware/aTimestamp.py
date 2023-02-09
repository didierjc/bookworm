from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from datetime import datetime


class asyncTimestamp(BaseHTTPMiddleware):
    def __init__(self, app,):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        # Getting the current date and time
        dt = datetime.now()

        # getting the timestamp
        ts = datetime.timestamp(dt)

        response.headers["X-DateAndTime"] = str(dt)
        response.headers["X-Timestamp"] = str(ts)

        return response
