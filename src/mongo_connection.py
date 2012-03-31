from pymongo import Connection
import config

class MongoConnection:
  def __init__(self):
    self.connection = Connection(config.MONGO_SERVER)
    self.db = self.connection[config.PUGG_DB]
