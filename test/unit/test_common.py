import config

config.PUGG_DB="pugg_test"
ALL_TESTS=[]

from mongo_connection import *
import json


class CommonSetup:
  @staticmethod
  def setupMongoDBFixtures():
    #load MediaCloud articles into mc_articles
    mongo_fixtures = json.load(open("test/fixtures/mediacloud/mediacloud_articles.json", "r"))
    for mongo_fixture in mongo_fixtures:
      MONGO_DB.mc_articles.insert(mongo_fixture)
  @staticmethod
  def teardownMongoDBFixtures():
    MONGO_DB.mc_articles.remove()
      
