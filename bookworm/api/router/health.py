from fastapi import APIRouter, status

from bookworm.api.model.health import Health


router = APIRouter(
    tags=["health"],
)


@router.get("/", status_code=status.HTTP_200_OK, response_model=Health)
async def health_check():
    '''
    Simple route for the GitHub Actions to health check on.

    More info is available at:
    https://github.com/akhileshns/heroku-deploy#health-check

    It basically sends a GET request to the route & hopes to get a "200"
    response code. Failing to return a 200 response code just enables
    the GitHub Actions to rollback to the last version the project was
    found in a "working condition". It acts as a last line of defense in
    case something goes south.
    
    Additionally, it also returns a JSON response in the form of:
    {
        ...
        'healthcheck': 'Everything OK!'
        ...
    }
    '''
    return Health()
