import redis 
import config
import hashlib

class Article:
  def __init__(self, init_dict = {}):
    self.puggdb = None
    self.article_id = None

    self.byline = init_dict['byline'] if init_dict.has_key('byline') else None
    self.pub_date = init_dict['pub_date'] if init_dict.has_key('pub_date') else None
    self.headline = init_dict['headline'] if init_dict.has_key('headline') else None
    self.filename = init_dict['filename'] if init_dict.has_key('filename') else None
    self.fulltext = init_dict['fulltext'] if init_dict.has_key('fulltext') else None
    self.word_count = init_dict['word_count'] if init_dict.has_key('word_count') else None
    self.source = init_dict['source'] if init_dict.has_key('source') else None

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
