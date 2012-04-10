from article import *
from string import *
from datetime import datetime
import time
from time import mktime

class MediaCloudArticle(Article):
  def __init__(self, init_dict):
    
    Article.__init__({
      "source": init_dict["media_name"],
      "headline": init_dict["title"],
      "byline": init_dict["author_name"],
    })
    self.pub_date = datetime.fromtimestamp(mktime(time.strptime(init_dict["publish_date"], "%Y-%m-%d %H:%M:%S")))
    self.byline = lower(self.byline.strip()).replace("by ", "")
    d = init_dict["pub_date"]
    self.pub_date = datetime.date(atoi(d[:4]), atoi(d[4:6]), atoi(d[6:]))
