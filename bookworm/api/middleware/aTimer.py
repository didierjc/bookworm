from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

import time

class asyncTimer(BaseHTTPMiddleware):
    def __init__(self, app,):
        super().__init__(app)

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        end_time = time.time() - start_time

        response.headers["X-Process-Time"] = str(end_time)

        return response
