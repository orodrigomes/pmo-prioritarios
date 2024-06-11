import os
import pathlib

from pydantic_settings import BaseSettings, SettingsConfigDict

DOTENV = pathlib.Path(os.path.dirname(__file__)).parent.joinpath('.env')


class Settings(BaseSettings):
    db_password: str
    db_user: str
    db_host: str
    db_database: str

    model_config = SettingsConfigDict(env_file=DOTENV)
