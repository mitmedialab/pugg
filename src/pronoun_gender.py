import csv
from nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize
from string import *
from nytimes_article import *
from nytimes_article_accessor import *

class PronounGender:
  def __init__(self, female_filename, male_filename):
    self.male_pronouns = []
    self.female_pronouns = []

    female_file = csv.reader(open(female_filename, "rb"))

    for pronoun in female_file:
      self.female_pronouns.append(pronoun[0].lower())

    male_file = csv.reader(open(male_filename, "rb"))
    for pronoun in male_file:
      self.male_pronouns.append( pronoun[0].lower())

  def estimate_gender(self, fulltext):
      male_count = 0
      female_count = 0
      for sentence in sent_tokenize(fulltext):
        for word in word_tokenize(sentence):
          word = word.lower()
          if word in self.female_pronouns:
            female_count += 1
          elif word in self.male_pronouns:
            male_count += 1
      if male_count + female_count == 0:
        return "U"
      male_percent = (float(male_count) / float(male_count + female_count))

      if male_percent > 0.66:
        return "M"
      elif male_percent > 0.33:
        return "N"
      else:
        return "F"
