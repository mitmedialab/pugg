import json, urllib
from nytimes_api_article import *

api_key = open("data/api_keys/nytimes.com.txt", "r").read()[:-1]
last_hour_url="http://api.nytimes.com/svc/news/v3/content/nyt/all/1.json?api-key=" + api_key

latest_articles = json.load(urllib.urlopen(last_hour_url))
if latest_articles["status"] == "OK" and latest_articles["num_results"] > 0:
  for article in latest_articles["results"]:
    db_article = NyTimesAPIArticle(article)
    print db_article.headline
    if db_article.exists_in_database() is None:
      db_article.save()
