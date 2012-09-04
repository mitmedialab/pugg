import couchdb
server = couchdb.Server()
db = server["dailymail"]
result = {}
for row in db.view('_design/bylines/_view/bylinereport'):
  article = row["value"]
  if not("sectionId" in article):
    article["sectionId"] = "none"
  if not (article["sectionId"] in result):
    result[article["sectionId"]] = 0
  result[article["sectionId"]] += 1

for section in result:
  print section

print result
