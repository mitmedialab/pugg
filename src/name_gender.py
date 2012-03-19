import csv
from string import *

class NameGender:
  def __init__(self, female_filename, male_filename):
    self.male_names = {}
    self.female_names = {}

    female_file = csv.reader(open(female_filename, "rb"))
    for name in female_file:
      self.female_names[name[0].lower()] = name[1]

    male_file = csv.reader(open(male_filename, "rb"))
    for name in male_file:
      self.male_names[name[0].lower()] = name[1]

  def estimate_gender(self, name):
    first_name = name.split(" ")[0].lower()
    male = self.male_names.has_key(first_name)
    female = self.female_names.has_key(first_name)
  
    if(male and female):
      difference = atoi(self.female_names[first_name][1]) - atoi(self.male_names[first_name][1])
      if difference > 0:
        return "F"
      else:
        return "M"
    elif female:
      return "F"
    elif male:
      return "M"
    else:
      return None
