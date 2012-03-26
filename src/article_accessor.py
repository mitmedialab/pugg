import redis
import config
from article import *

class ArticleAccessor:
  def __init__(self, data):
    self.current_redis_index = 0
    self.puggdb = None
 
  def establishConnection(self):
    if self.puggdb == None:
      self.puggdb = redis.Redis(config.REDIS_SERVER, db=config.PUGG_DB)
    return self.puggdb

  #returns an article
  def getNextRedisArticle(self):
    self.establishConnection()
    if self.current_redis_index >= self.puggdb.llen("article.keys"):
      return None
    article_id = self.puggdb.lindex("article.keys", self.current_redis_index)
    article_key = "article:"+article_id+":"

    article_dict = {}
    for field_name in Article.redisFields():
      article_dict[field_name] = self.puggdb.get(article_key + field_name)
    self.current_redis_index += 1
    return Article(article_dict)
      
  
  def createArticle(self, row):
    print "Accessing ArticleAccessor: Please Access Inherited Class"
  def getNextArticle(self):
    print "Accessing ArticleAccessor: Please Access Inherited Class"
  def getNextMonth(self):
    print "Accessing ArticleAccessotr: Please Access Inherited Class"
