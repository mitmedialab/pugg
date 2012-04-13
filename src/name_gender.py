import csv
from string import *

class NameGender:
  def __init__(self, female_filename, male_filename, female_suppl = None, male_suppl = None):
    self.male_names = {}
    self.female_names = {}
    self.male_supplement = []
    self.female_supplement = []

    female_file = csv.reader(open(female_filename, "rb"))
    for name in female_file:
      self.female_names[name[0].lower()] = name[1]

    male_file = csv.reader(open(male_filename, "rb"))
    for name in male_file:
      self.male_names[name[0].lower()] = name[1]

    if female_suppl is not None:
      female_suppl_file = csv.reader(open(female_suppl))
      for name in female_suppl_file:
        if len(name) ==0: 
          continue
        self.female_supplement.append(name[0].lower())

    if male_suppl is not None:
      male_suppl_file = csv.reader(open(male_suppl))
      for name in male_suppl_file:
        if len(name) ==0: 
          continue
        self.male_supplement.append(name[0].lower())

  def check_gender(self, name):
    first_name = name.split(" ")[0].lower()
    male = self.male_names.has_key(first_name)
    female = self.female_names.has_key(first_name)
    if(male and female):
      return None
    elif male:
      return "M"
    elif female:
      return "F"
    return None

  def estimate_gender(self, name):
    first_name = name.split(" ")[0].lower()
    male = self.male_names.has_key(first_name)
    female = self.female_names.has_key(first_name)
  
    if(male and female):
      try:
        female_count = atof(self.female_names[first_name])
      except ValueError:
        female_count = 0
      try:
        male_count = atof(self.male_names[first_name])
      except ValueError:
        male_count = 0 

      total = female_count + male_count
      prob_female = float(female_count) / float(total)
      prob_male = float(male_count) / float(total)
      if prob_female > 0.65:
        return "F"
      elif prob_male > 0.65:
        return "M"
      else:
        return None
    elif female:
      return "F"
    elif male:
      return "M"
    else:
      #now try to the supplementary gender data
      try:
        if self.male_supplement.index(first_name):
          return "M"
      except ValueError:
        pass
      try:
        if self.female_supplement.index(first_name):
          return "F"
      except ValueError:
        pass
          
      return None
