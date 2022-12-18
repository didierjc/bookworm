from fastapi import APIRouter, status

from bookworm.api.model.health import Health


router = APIRouter(
    tags=["health"],
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=Health)
async def health_check():
    """Application health check endpoint"""
    return Health()
