from article import *
from string import *
from datetime import datetime
import time
from time import mktime

class MediaCloudArticle(Article):
  def __init__(self, init_dict):
    Article.__init__(self, dict({
      "source": init_dict["media_name"],
      "headline": init_dict["title"],
      "byline": init_dict["author_name"],
      "fulltext": init_dict["description"]
    }.items() + init_dict.items()))
    self.articles = self.db.mediacloud_articles
    self.pub_date = datetime.fromtimestamp(mktime(time.strptime(init_dict["publish_date"], "%Y-%m-%d %H:%M:%S")))
    self.byline = lower(self.byline.strip()).replace("by ", "")
    #self.collect_date =  datetime.fromtimestamp(mktime(time.strptime(init_dict["collect_date"], "%Y-%m-%d %H:%M:%S")))
    #self.guid = init_dict["guid"]
