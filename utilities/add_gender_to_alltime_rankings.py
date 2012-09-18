from name_gender import *
from sys import *
from glob import glob
import re
import csv
import os.path

genderer = NameGender("data/names/female_names_EN_GB.csv", "data/names/male_names_EN_GB.csv", "data/names/female_auxilliary_EN_GB.csv", "data/names/male_auxilliary_EN_GB.csv")


##### USAGE ######
#python utilities/add_gender_to_rankings.py input.csv output.csv
filename = argv[1]
row_count = 0
output_file = argv[2]
output = csv.writer(open(output_file, "wb"))
output.writerow(["byline","gender",
                 "articles","facebook","googleplus","twitter", "total popularity", "avg popularity"])

with open(filename, 'rb') as f:
  print filename
  reader = csv.reader(f)
  for row in reader:
    if row_count == 0:
      row_count +=1
      continue
    if len(row) <6:
        print row #FIX THIS
        continue

    row_count += 1
    return_row = []
    return_row.append(row[0]) #byline
    byline = row[0].lower().strip()
    if( re.search("press",byline) or re.search("reuters", byline) or 
      re.search("agencies", byline) or re.search("associated press",byline) or 
      byline =="ap" or byline =="" or
      (re.search("editor", byline) and len(byline.split(" ")) <=3) or 
      (re.search("correspondent", byline) and len(byline.split(" ")) <=3 ) or
      re.search("staff", byline) or len(byline) == 0 or
      re.search("reporter", byline) or re.search("daily mail", byline) or
      re.search("this is money", byline) or re.search("money mail", byline)):
      gender ="X"
    else:
      gender = genderer.estimate_gender(byline)
      if(gender == None):
        gender = "N"
    return_row.append(gender) #gender
    return_row.append(row[1]) #articles
    return_row.append(row[2]) #facebook
    return_row.append(row[3]) #googleplus
    return_row.append(row[4]) #twitter
    return_row.append(row[5]) #total popularity
    return_row.append(row[6]) #avg popularity

    output.writerow(return_row)
