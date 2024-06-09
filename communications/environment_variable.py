"""Environment variables."""

from os import getenv
from uuid import uuid4

from dotenv import load_dotenv

load_dotenv()


MODE = getenv('MODE', 'development')
EMPTY_VALUE = str(uuid4())
DEFAULT_REDIS_PORT = '6379'
DEFAULT_DB_PORT = '5432'


class Envs:
    """Envs."""

    IS_DEVELOPMENT = MODE == 'development'
    IS_PRODUCTION = MODE == 'production'
    SECRET_KEY = getenv('SECRET_KEY', EMPTY_VALUE)

    REDIS_HOST = getenv('REDIS_HOST', '127.0.0.1')
    REDIS_PORT = getenv('REDIS_PORT', DEFAULT_REDIS_PORT) if IS_DEVELOPMENT else DEFAULT_REDIS_PORT

    DB_NAME = getenv('DB_NAME', EMPTY_VALUE)
    DB_USER = getenv('DB_USER', EMPTY_VALUE)
    DB_PASSWORD = getenv('DB_PASSWORD', EMPTY_VALUE)
    DB_HOST = getenv('DB_HOST', '127.0.0.1')
    DB_PORT = getenv('DB_PORT', DEFAULT_DB_PORT) if IS_DEVELOPMENT else DEFAULT_DB_PORT


for evns_property in dir(Envs):
    if getattr(Envs, evns_property) == EMPTY_VALUE:
        raise ValueError(f'Not defined {evns_property} in .env file!')
