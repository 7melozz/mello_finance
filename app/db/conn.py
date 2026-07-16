import os
import urllib.parse

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

load_dotenv()

REQUIRED_ENV_VARS = [
    "DB_USER",
    "DB_PASSWORD",
    "DB_HOST",
    "DB_PORT",
    "DB_NAME",
]


def _require_env(name):
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value


def get_database_url():
    explicit_url = os.getenv("DATABASE_URL")
    if explicit_url:
        return explicit_url

    user = urllib.parse.quote_plus(_require_env("DB_USER"))
    password = urllib.parse.quote_plus(_require_env("DB_PASSWORD"))
    host = _require_env("DB_HOST")
    port = _require_env("DB_PORT")
    db_name = _require_env("DB_NAME")

    return f"postgresql://{user}:{password}@{host}:{port}/{db_name}"


DATABASE_URL = get_database_url()


engine = create_engine(DATABASE_URL, future=True)


SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    future=True,
)
