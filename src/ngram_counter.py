from nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize
from string import *
import re

class WordCounter: # Looks for single words in article fulltexts
    def __init__(self, phrases, papa_dir):
    # phrases is list of lower-case words to be searched for,
    # papa_dir is string of directory where the txt files to be searched are
    #   (sorted into sub-directory by year: each named "1987" through "2006")
    #   in which female obituaries are named by index: 0.txt, 1.txt, so on.
    #   papa_dir must also contain empty directory named "results".
        self.papa_dir = papa_dir
        self.phrases = phrases
        
        # This dictionary will be used when calculating phrase use/total articles
        self.yearly_female_obit_totals = {1987: 293, 1988: 338, \
                                          1989: 415, 1990: 456, \
                                          1991: 375, 1992: 369, \
                                          1993: 320, 1994: 312, \
                                          1995: 327, 1996: 329, \
                                          1997: 268, 1998: 263, \
                                          1999: 238, 2000: 235, \
                                          2001: 232, 2002: 223, \
                                          2003: 193, 2004: 187, \
                                          2005: 156, 2006: 193}

        # This dictionary will be used when calculating phrase use/total words
        self.yearly_allword_totals = {1987: 93494, 1988: 98204, \
                                          1989: 119915, 1990: 149492, \
                                          1991: 119066, 1992: 136511, \
                                          1993: 120013, 1994: 116375, \
                                          1995: 135716, 1996: 163163, \
                                          1997: 152117, 1998: 174124, \
                                          1999: 143830, 2000: 148206, \
                                          2001: 156630, 2002: 157607, \
                                          2003: 126611, 2004: 123912, \
                                          2005: 105244, 2006: 158888} 
        
      # Create a dictionary mapping phrases to (boolean, int)
      # for marking and counting occurrences of that phrase.
      # bool, number of articles using that phrase, num articles phrase/total num articles,
      #   total phrase uses/total words, total phrase uses
        self.phrase_counter = {phrase: [False, 0, 0, 0, 0] for phrase in phrases}

        self.phrase_fulltext_dict = {} # For .txt's to store relevant fulltext


    def count_words(self):
      # Create 20 txt files (one per year) associated with each phrase in which
      # to store fulltexts that contain that phrase.
      # Must access using dict[phrase][year-1987]
        line = "year,total_fem_obit,total_words" 
        for phrase in self.phrases:
        ###    self.phrase_fulltext_dict[phrase] = \
        ###        [open(self.papa_dir+'/results/'+phrase+'_'+str(i)+'.txt', 'w')\
        ###         for i in range(1987, 2007)]
            line = line +','+phrase+'_count'+','+'articles_containing_'+phrase+'/total_articles'+','+phrase+'_uses/total_words'

        print line

        for year in range(1987, 2007):
            for article_index in range(self.yearly_female_obit_totals[year]):
                current_file = open(self.papa_dir+'/'+str(year)+'/'+str(article_index)+'.txt', 'r')
                fulltext = current_file.read()
                for sentence in sent_tokenize(fulltext):
                    for word in word_tokenize(sentence):
                        word = word.lower()
                        if word in self.phrases:
                            self.phrase_counter[word][4] += 1
                            if not self.phrase_counter[word][0]:
                                self.phrase_counter[word][0] = True
                                ###self.phrase_fulltext_dict[word][year-1987].write(re.sub('\n', ' ', fulltext)+'\n')
                current_file.close()
                # Increment phrase count and reset phrase bool to false
                for phrase in self.phrases:
                    if self.phrase_counter[phrase][0]:
                        self.phrase_counter[phrase][1] += 1
                    self.phrase_counter[phrase][0] = False

            # Calculate and store phrase-use-rates
            for phrase in self.phrases:
                self.phrase_counter[phrase][2] = \
                        self.phrase_counter[phrase][1] / \
                        float(self.yearly_female_obit_totals[year])
                self.phrase_counter[phrase][3] = \
                        self.phrase_counter[phrase][4] / \
                        float(self.yearly_allword_totals[year])
                ###self.phrase_fulltext_dict[phrase][year-1987].close()

            # Print counts & rates and reset all count variables to 0
            line = str(year)+','+str(self.yearly_female_obit_totals[year])+','+str(self.yearly_allword_totals[year])
            for phrase in self.phrases:
                line = line +','+str(self.phrase_counter[phrase][1])+','+ \
                       str(self.phrase_counter[phrase][2])+','+ \
                       str(self.phrase_counter[phrase][3])+','+ \
                       str(self.phrase_counter[phrase][4])
                self.phrase_counter[phrase] = [False, 0, 0, 0, 0]
                
            print line

    def count_total_words(self):
        print "year,word_total,avg_obit_length_in_words"
        for year in range(1987, 2007):
            word_total = 0
            for article_index in range(self.yearly_female_obit_totals[year]):
                current_file = open(self.papa_dir+'/'+str(year)+'/'+str(article_index)+'.txt', 'r')
                fulltext = current_file.read()
                for sentence in sent_tokenize(fulltext):
                    for word in word_tokenize(sentence):
                        word_total += 1
                        current_file.close()
            print str(year)+','+str(word_total)+','+str(word_total/float(self.yearly_female_obit_totals[year]))

                
            
if __name__ == "__main__":
    word_counter = WordCounter(["married", "founded", "research"], "obits_fem")
    word_counter.count_total_words()