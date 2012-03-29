import hashlib

class Article:
  def __init__(self, init_dict = {}):
    self.puggdb = None
    self.article_id = None

    self.source = init_dict['source'] if init_dict.has_key('source') else None
    self.headline = init_dict['headline'] if init_dict.has_key('headline') else None
    self.byline = init_dict['byline'] if init_dict.has_key('byline') else None
    self.pub_date = init_dict['pub_date'] if init_dict.has_key('pub_date') else None
    self.filename = init_dict['filename'] if init_dict.has_key('filename') else None
    self.fulltext = init_dict['fulltext'] if init_dict.has_key('fulltext') else None
    self.word_count = init_dict['word_count'] if init_dict.has_key('word_count') else None

  def articleFields():
    return ["source", "headline", "byline", "pub_date", "filename", "fulltext", "word_count"]
  articleFields = staticmethod(articleFields)
