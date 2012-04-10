import config
from nytimes_article_accessor import *

config.PUGG_DB="pugg_test"
ALL_TESTS=[]

from mongo_connection import *
import json


class CommonSetup:
  @staticmethod
  def setupMediaCloudFixtures():
    #load MediaCloud articles into mc_articles
    mongo_fixtures = json.load(open("test/fixtures/mediacloud/mediacloud_articles.json", "r"))
    for mongo_fixture in mongo_fixtures:
      MONGO_DB.mc_articles.insert(mongo_fixture)
  @staticmethod
  def teardownMediaCloudFixtures():
    MONGO_DB.mc_articles.remove()
      
  @staticmethod
  def setupNYTimesFixtures():
    article_accessor = NYTimesArticleAccessor("test/fixtures/nytimes")
    article = article_accessor.createArticle(article_accessor.getNextArticle())
    while(article):
      article.fulltext = article.getDataFileObject("data/full/", "test/fixtures/nytimes-data/", "txt").read()
      article.save()
      try:
        article = article_accessor.createArticle(article_accessor.getNextArticle())
      except ValueError:
        continue
      except TypeError:
        break

  @staticmethod
  def teardownNYTimesFixtures():
    MONGO_DB.articles.remove()
