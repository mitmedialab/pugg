import MySQLdb as mdb
from name_gender import *
import re

#format bylines scraped from ProQuest
def format_byline(byline):
  if(byline is None or byline.strip() == ""):
    #no_byline += 1
    return None

  #total_bylines += 1
  byline = byline.lower()
  match_by = re.search('.*(by)(.*)', byline)
  if(match_by):
    #includes_by += 1
    byline = match_by.group(2).strip()

  match_multiple_authors = re.search('(.*?);(.*)', byline)
  if(match_multiple_authors):
  #  multiple_authors += 1
    byline = match_multiple_authors.group(1)
  
  match_reverse_bylines = re.search('(.*?),(.*)', byline)
  if(match_reverse_bylines):
    first_token = match_reverse_bylines.group(1).strip()
    #  reverse_bylines += 1
    if len(first_token.split(" "))>1:
      byline = first_token
    else:
      byline = match_reverse_bylines.group(2).strip() + " " + match_reverse_bylines.group(1).strip()

  return byline

#the main script begins here
total_articles = none = female = male = byline_count = no_bylines = 0

genderer = NameGender("data/names/female_names.csv", "data/names/male_names.csv", "data/names/female_auxilliary.csv", "data/names/male_auxilliary.csv")

connection = mdb.connect("localhost", "usworld", "", "usworld_dev")
cursor = connection.cursor()
cursor.execute("SELECT id, byline FROM articles;")
bylines = cursor.fetchall()


for byline_row in bylines:
  total_articles += 1
  byline_id = byline_row[0]
  byline = format_byline(byline_row[1])

  if(byline is None or len(byline.strip()) == 0):
    no_bylines += 1
  else:
    byline_count += 1
    gender = genderer.estimate_gender(byline)
    if(gender == "M"):
      male += 1
    elif(gender == "F"):
      female += 1
    else:
      gender = None
      none += 1

  #now update the record
  try:
    cursor.execute("UPDATE articles set gender=%s where id=%s;", (gender, str(byline_id)))
  except TypeError:
    import pdb;pdb.set_trace()

connection.commit()

print "total fields: " + str(total_articles)
print "bylines: " + str(byline_count)
print "no bylines " + str(no_bylines)
print "female: " + str(female)
print "male: " + str(male)
print "no match:" + str(none)
