import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MONGO_URI: str = "mongodb://mongo:27017"

settings = Settings()
