import csv
import glob
from article_accessor import *
from nytimes_article import *

class NYTimesArticleAccessor(ArticleAccessor):
  def __init__(self, data_dir):
    ArticleAccessor.__init__(self, data_dir)
    self.data_dir = data_dir
    self.csv_filenames = glob.glob(data_dir + "/*")
    self.csv_filenames.sort()
    self.current_file = None
    self.nyt_csv_reader = None

  #metadata_keys defined in nyt ruby library app/models/article.rb
  def createArticle(self, row):
    return NYTimesArticle({'pub_date': row[0],
      'bylines': row[1],
      'datline': row[2], 
      'descriptors': row[3],
      'taxonomic_classifiers': row[4],
      'locations': row[5],
      'page': row[6],
      'section': row[7],
      'column': row[8],
      'news_desk': row[9],
      'word_count': row[10],
      'headline': row[11],
      'filename': row[12]})
      

  def getNextArticle(self):
    if self.nyt_csv_reader == None:
      load_success = self.loadNextMonth()
      if not load_success:
        return None
    try:
      return self.nyt_csv_reader.next()
    except StopIteration:
      self.nyt_csv_reader = None
      return self.getNextArticle()

  def getNextMonth(self):
    load_success = self.loadNextMonth()
    if not load_success:
      return None
    rows = []
    for row in self.nyt_csv_reader:
      rows.append(row)
    self.nyt_csv_reader = None
    return rows

  def loadNextMonth(self):
    self.current_file = 0 if self.current_file == None else self.current_file + 1
    if self.current_file != None and self.current_file >= len(self.csv_filenames):
      return None
    current_filename = self.csv_filenames[self.current_file]
    self.nyt_csv_reader = csv.reader(open(current_filename, 'rb'))
    return 1
