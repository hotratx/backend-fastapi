from pydantic import BaseSettings


class Settings(BaseSettings):
    # Base
    api_v1_prefix: str
    debug: bool
    project_name: str
    version: str
    description: str
    # Database
    db_async_connection_str: str
    database_port: str
    postgres_password: str
    postgres_user: str
    postgres_host: str
    postgres_db: str
    postgres_hostname: str
    db_async_test_connection_str: str
    # Tests
    tests: bool
    # token
    access_expiration: int
    refresh_expiration: int
    private_key: str
    # Cache
    url_cache: str
