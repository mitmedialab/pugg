import csv
import glob

class NYTimesArticleAccessor:
  def __init__(self, data_dir):
    self.data_dir = data_dir
    self.csv_filenames = glob.glob(data_dir + "/*")
    self.csv_filenames.sort()
    self.current_file = None
    self.nyt_csv_reader = None

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
