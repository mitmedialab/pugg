from pymongo import Connection
import config

MONGO_CONNECTION = Connection(config.MONGO_SERVER)
MONGO_DB = MONGO_CONNECTION[config.PUGG_DB]
