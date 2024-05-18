# for db credentials from environment variables in .env or any other source

from pydantic_settings import BaseSettings # to define a Settings class to hold configuration data (db credentials).

class Settings(BaseSettings): #env var are case insensitive by pydantic. 
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    # tells pydantic to read env vars from .env
    class Config:
        env_file = ".env"
        extra = "allow" # allows non alembic variables to exist in .env
  
settings = Settings()    # holds the actual configuration data (db credentials)