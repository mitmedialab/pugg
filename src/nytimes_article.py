from article import *
from string import *
import datetime

class NYTimesArticle(Article):
  def __init__(self, init_dict):
    Article.__init__(self)
    self.bylines = init_dict["bylines"].split("|")
    self.byline = lower(self.bylines[0]).replace("by ", "")

    d = init_dict["pub_date"]
    self.pub_date = datetime.date(atoi(d[:4]), atoi(d[4:6]), atoi(d[6:]))

    self.headline = init_dict["headline"]
    self.locations = init_dict["locations"]
    self.filename = init_dict["filename"]
    self.taxonomic_classifiers = init_dict["taxonomic_classifiers"].split("|")
    self.source = "NYTimes"
    self.fulltext = None
