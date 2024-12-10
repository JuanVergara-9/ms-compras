import os
import redis

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'postgresql+psycopg2://postgres:12345678@localhost:5432/compras_bd')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
    r = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0)