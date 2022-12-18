from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from bookworm.api.router import health
from bookworm.api.middleware.aTimer import asyncTimer
from bookworm.api.middleware.aLogRequests import asyncLogRequests

# Create FastAPI instance
api = FastAPI()

# Add gzip compression
api.add_middleware(GZipMiddleware, minimum_size=1000)
# Add trusted hosts
api.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])
# Add timer
api.add_middleware(asyncTimer)
# Add request logger
api.add_middleware(asyncLogRequests)

# Add routers
api.include_router(health.router, prefix="/health", tags=["health"], responses={404: {"description": "Not found"}})

# Add root endpoint
@api.get("/", status_code=200)
def home():
    return {"status_code": 200, "status": "Ok"}
