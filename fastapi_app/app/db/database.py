from sqlmodel import SQLModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.ext.asyncio import AsyncEngine
from typing import AsyncGenerator
import os
from urllib.parse import quote
import socket
from pydantic_settings import BaseSettings
import psycopg


class Settings(BaseSettings):
    """Configuration settings for the application from environment variables."""
    POSTGRESQL_USER: str = "postgres"
    POSTGRESQL_PASSWD: str = "password"
    POSTGRESQL_HOST: str = "localhost"
    TEST_API: bool = False

    model_config = {
        "extra": "allow",  # Allow extra fields in the environment
        "env_file": "../.env",  # Load environment variables from a .env file
    }


# read settings from environment variables
settings = Settings()


def build_database_url(settings: Settings, database):
    """
    Builds a PostgreSQL database URL for SQLAlchemy using provided settings and database name.

    Args:
        settings: An object containing PostgreSQL connection attributes (POSTGRESQL_USER, POSTGRESQL_PASSWD, POSTGRESQL_HOST).
        database (str): The name of the database to connect to.

    Returns:
        str: A formatted PostgreSQL database URL with credentials and SSL mode enabled.
    """
    # Quote the user and password to handle special characters
    user = quote(settings.POSTGRESQL_USER)
    passwd = quote(settings.POSTGRESQL_PASSWD)
    return f"postgresql+psycopg://{user}:{passwd}@{settings.POSTGRESQL_HOST}:5432/{database}"


def ensure_databases_exists(settings: Settings):
    """
    Ensures that the required PostgreSQL databases ('tracker' and 'tracker_test') exist, creating them if necessary.
    If the 'TEST_API' setting is enabled, connects to the 'tracker_test' database and resets its schema by dropping and recreating the 'public' schema.
    Args:
        settings (Settings): An object containing PostgreSQL connection parameters and configuration flags.
    Side Effects:
        - Connects to the PostgreSQL server as an admin user.
        - Creates the 'tracker' and 'tracker_test' databases if they do not exist.
        - Optionally resets the schema in the 'tracker_test' database if 'TEST_API' is True.
    """
    print("Connecting to default database...")

    with psycopg.connect(
        dbname="postgres",
        user=settings.POSTGRESQL_USER,
        password=settings.POSTGRESQL_PASSWD,
        host=settings.POSTGRESQL_HOST,
        autocommit=True  # Required for CREATE DATABASE
    ) as admin_conn, admin_conn.cursor() as cur:

        for db in ["tracker", "tracker_test"]:

            # Check if the database already exists
            cur.execute(
                f"SELECT 1 FROM pg_database WHERE datname = %s;", (db,))
            exists = cur.fetchone()

            if not exists:
                print(f"Creating database {db}...")
                cur.execute(f'CREATE DATABASE "{db}";')
            else:
                print(f"Database {db} already exists.")

    if settings.TEST_API:
        # Step 2: Connect to the test database and wipe it
        print(f"Connecting to test database 'tracker_test'...")
        with psycopg.connect(
            dbname='tracker_test',
            user=settings.POSTGRESQL_USER,
            password=settings.POSTGRESQL_PASSWD,
            host=settings.POSTGRESQL_HOST,
            autocommit=True
        ) as test_conn, test_conn.cursor() as cur:
            print(f"Resetting schema in 'tracker_test'...")
            cur.execute("DROP SCHEMA public CASCADE; CREATE SCHEMA public;")


# Ensure the required databases exist
ensure_databases_exists(settings)

if settings.TEST_API:
    DATABASE_URL = build_database_url(settings, "tracker_test")
else:
    DATABASE_URL = build_database_url(settings, "tracker")

print(f"Connecting to database at {DATABASE_URL}")

engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=True)
async_session = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False)


async def create_db_and_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session
