from dataclasses import dataclass

from dotenv import load_dotenv
import os

load_dotenv()


# data_base
@dataclass
class DbConfig:
    host: str
    port: str
    name: str
    user: str
    password: str


db_config = DbConfig(
    host=os.environ.get("DB_HOST"),
    port=os.environ.get("DB_PORT"),
    name=os.environ.get("DB_NAME"),
    user=os.environ.get("DB_USER"),
    password=os.environ.get("DB_PASS"),
)


# jwt secret key
@dataclass
class Jwt:
    jwt: str
    algorithm: str


jwt_key = Jwt(
    jwt=os.environ.get("JWT_SECRET_KEY")
    , algorithm=os.environ.get("ALGORITHM")
)


# redis
@dataclass
class RedisConfig:
    host: str
    port: str


redis_config = RedisConfig(
    host=os.environ.get("REDIS_HOST"),
    port=os.environ.get("REDIS_PORT")
)
