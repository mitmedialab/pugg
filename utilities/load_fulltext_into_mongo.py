from time import time
import sys
from mongo_connection import *
from nytimes_article_accessor import *
from article import *

class LoadFullTextIntoMongo:
  def __init__(self):
    self.loadFullText()

  def loadFullText(self, limit = 200000000000):
    self.db = MONGO_DB
    count = 0 
    for article_dict in self.db.articles.find():
      article = Article(article_dict)
      article_dict["fulltext"] = article.getDataFileObject("data/full/", "data/nytimes-fulltext/", "txt").read()
      
      self.db.articles.save(article_dict)
      test = self.db.articles.find_one(article_dict)
      if count >= limit:
        break
      if count % 100 == 0:
         print ".",
         sys.stdout.flush()
      count += 1
if __name__ == "__main__":
  benchmark = LoadFullTextIntoMongo()
