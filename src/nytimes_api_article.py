from article import *
from string import *
from datetime import datetime
import time
from time import mktime

class NyTimesAPIArticle(Article):
  def __init__(self, init_dict):
    Article.__init__(self, dict({
      "headline": init_dict["title"],
    }.items() + init_dict.items()))
    self.articles = self.db.nytimes_api_articles
    self.pub_date = datetime.fromtimestamp(mktime(time.strptime(init_dict["created_date"][:-6], "%Y-%m-%dT%H:%M:%S")))
    self.byline = lower(self.byline.lower().strip()).replace("by ", "")
    self.url = init_dict["url"]

  def exists_in_database(self):
    return self.articles.find_one({'url': self.url})
  
  def save(self):
    Article.save(self, {'url': self.url})
