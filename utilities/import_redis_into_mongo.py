from mongo_connection import *
import redis

count = 0
r = redis.StrictRedis(host="97.107.131.246", port=6379, db=0)
article_keys = r.keys("*")
for article_key in article_keys:
  article = r.hgetall(article_key)
  MONGO_DB.mc_articles.save(article)
  count += 1
  if count % 100 == 0:
    print count
