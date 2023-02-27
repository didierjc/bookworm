from dotenv import load_dotenv
from fastapi import APIRouter, status

from bookworm.api.model.health import Health, HealthDB
from bookworm.api.service.customLog import CustomLog

import os

# Load environment variables without exporting the variables explicitly by the export command
load_dotenv()


router = APIRouter(
    tags=["health"],
)

log = CustomLog()


@router.get("/", status_code=status.HTTP_200_OK, response_model=Health)
async def health_check():
    """
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
    """
    return Health()


@router.get("/checkdb", status_code=status.HTTP_200_OK, response_model=HealthDB)
async def health_check_db():
    """
    Simple route for the database health check.
    """
    import psycopg
    from psycopg import Error

    connection = None

    try:
        columns = ("column",)
        results = []

        # Connect to an existing database
        connection = psycopg.connect(
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
        )

        # Create a cursor to perform database operations
        cursor = connection.cursor()

        # Executing a SQL query
        cursor.execute("select 1;")

        # Fetch result & convert to JSON
        results.append(dict(zip(columns, cursor.fetchone())))

        log.logThis(
            "health.health_check_db",
            f"database message: {HealthDB(message=str(results),)}",
        )
        return HealthDB(
            message=str(results),
        )

    except (Exception, Error) as err:
        log.logThis("health.health_check_db", str(err), "error")

        return HealthDB(
            healthcheck="Database connection failed.",
            active=False,
            status=500,
            message=str(err),
        )

    # a finally clause is always executed before leaving the try statement, whether an exception has occurred or not...
    finally:
        if connection:
            cursor.close()
            connection.close()
