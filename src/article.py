import hashlib
from mongo_connection import *

class Article:
  def __init__(self, init_dict = {}):
    self.db = MONGO_DB
    self.db.articles
    self.db_object = init_dict

    self.source = init_dict['source'] if init_dict.has_key('source') else None
    self.headline = init_dict['headline'] if init_dict.has_key('headline') else None
    self.byline = init_dict['byline'] if init_dict.has_key('byline') else None
    self.pub_date = init_dict['pub_date'] if init_dict.has_key('pub_date') else None
    self.filename = init_dict['filename'] if init_dict.has_key('filename') else None
    self.fulltext = init_dict['fulltext'] if init_dict.has_key('fulltext') else None
    self.word_count = init_dict['word_count'] if init_dict.has_key('word_count') else None

  def save(self):
    article = {'source': self.source,
               'headline': self.headline,
               'byline': self.byline,
               'pub_date': str(self.pub_date),
               'filename': self.filename,
               'fulltext': self.fulltext,
               'wordcount': self.word_count}
    if self.db_object:
      self.db_object = self.db.articles.find_one(self.db_object)
      for key in article.iterkeys():
        self.db_object[key] = article[key]
      self.db.articles.save(self.db_object)
    else:
      self.db_object = self.db.articles.insert(article)

  def articleFields():
    return ["source", "headline", "byline", "pub_date", "filename", "fulltext", "word_count"]
  articleFields = staticmethod(articleFields)

  def getDataFileObject(self, orig_dir, data_dir, extension):
    data_filename = self.filename.replace("data/full/", data_dir).replace("xml", extension)
    return open(data_filename, "r")
