from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class Health(BaseModel):
    """Health model"""

    title: str = "Bookworm API: Health Check"
    status: int = 200
    healthcheck: Optional[str] = "Everything OK!"
    active: Optional[bool] = True
    message: Optional[str] = None
    timestamp: Optional[datetime] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # type: ignore


class HealthDB(BaseModel):
    """Database Health model"""

    title: str = "Bookworm API: Database Health Check"
    status: int = 200
    healthcheck: Optional[str] = "Everything OK!"
    active: Optional[bool] = True
    message: Optional[str] = None
    timestamp: Optional[datetime] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # type: ignore
    