import redis
import time

mc_redis = redis.Redis("97.107.131.246")

while 1:
  queue_keys = mc_redis.keys("*")
  if len(queue_keys) > 0:
    queue_keys.sort()
    article = mc_redis.hgetall(queue_keys[0])
    print article["publish_date"] + " - " + article["title"]
    print "   " + article["url"]
    
    mc_redis.delete(queue_keys[0])
  else:
    print "."
  sleep(2)
