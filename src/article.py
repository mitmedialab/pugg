import redis 
import config
import hashlib

class Article:
  def __init__(self):
    self.puggdb = None
    self.article_id = None

    self.byline = None
    self.pub_date = None
    self.headline = None
    self.filename = None
    self.fulltext = None
    self.word_count = None
    self.source = None
    self.filename = None

  def establishConnection(self):
    if self.puggdb == None:
      self.puggdb = redis.Redis(config.REDIS_SERVER, db=config.PUGG_DB)
      self.article_id = hashlib.sha1(str(self.pub_date) + self.headline + self.source).hexdigest()
    return self.puggdb

  def save(self, overwrite = 1):
    self.establishConnection()
    if overwrite or self.puggdb.lindex("article.keys", self.article_id):
      if self.puggdb.lindex("article.keys", self.article_id) == None:
        self.puggdb.lpush("article.keys", self.article_id)
      self.puggdb.set(self.rs("source"), self.source)
      self.puggdb.set(self.rs("headline"), self.headline)
      self.puggdb.set(self.rs("byline"), self.byline)
      self.puggdb.set(self.rs("pub_date"), self.pub_date)
      self.puggdb.set(self.rs("fulltext"), self.fulltext)
      self.puggdb.set(self.rs("filename"), self.filename)
      self.puggdb.set(self.rs("word_count"), self.word_count)

  def rs(self, key):
    return "article:" + self.article_id + ":" + key
