from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class Health(BaseModel):
    """Health model"""
    title: str = 'Bookworm API: Health Check'
    status: int = 200
    message: Optional[str] = 'We are alive!'
    active: Optional[bool] = True
    timestamp: Optional[datetime] = datetime.now().strftime('%Y-%m-%d %H:%M:%S') # type: ignore
