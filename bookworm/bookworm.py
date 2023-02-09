from datetime import datetime
from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from bookworm.api.router import health
from bookworm.api.middleware.aTimer import asyncTimer
from bookworm.api.middleware.aTimestamp import asyncTimestamp
from bookworm.api.middleware.aLogRequests import asyncLogRequests

from bookworm.config.settings import settings

# Load environment variables without exporting the variables explicitly by the export command
load_dotenv()


# Create FastAPI instance
api = FastAPI()

# Add gzip compression
api.add_middleware(GZipMiddleware, minimum_size=1000)
# Add trusted hosts
api.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])
# Add timer
api.add_middleware(asyncTimer)
# Add timestamp
api.add_middleware(asyncTimestamp)
# Add request logger
api.add_middleware(asyncLogRequests)

# Add routers
api.include_router(
    health.router,
    prefix="/health",
    tags=["health"],
    responses={404: {"description": "Not found"}},
)

# Add root endpoint
@api.get("/", status_code=200)
def home():
    meta = {
        "version": settings.VERSION,
        "timestamp": datetime.timestamp(datetime.now()),
        "environment": settings.ENV_STATE,
    }
    return {
        "running": True,
        "app_name": settings.APP_NAME,
        "debug": settings.DEBUG,
        "status_code": 200,
        "status": "Ok",
        "test": settings.TEST,
        "logging": settings.LOG_LEVEL,
        "meta": meta,
    }
