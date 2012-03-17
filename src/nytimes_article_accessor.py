import csv
import glob

class NYTimesArticleAccessor:
  def __init__(self, data_dir):
    self.data_dir = data_dir
    self.csv_filenames = glob.glob(data_dir + "/*")
    self.current_file = None
    self.nyt_csv_reader = None

  def getNextArticle(self):
    print "Accessing ArticleAccessor: Please Access Inherited Class"

  def getNextMonth(self):
    self.current_file = 0 if self.current_file == None else self.current_file + 1
    if self.current_file != None and self.current_file >= len(self.csv_filenames):
      return None

    current_filename = self.csv_filenames[self.current_file]
    self.nyt_csv_reader = csv.reader(open(current_filename, 'rb'))
    rows = []
    for row in self.nyt_csv_reader:
      rows.append(row)
    self.nyt_csv_reader = None
    return rows
