import json
from nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize
from string import *
import re
from operator import itemgetter

# Draw the Raphael lines, top line and bottom line,
#  to go around the sentence divs and designate the graph.
# heights is a list of the heights of the 20 sentence divs.
# width is the width, in pixels, of the divs.
# spacing is the space, in pixels, between the divs; width
#  of the raphael curves will equal to spacing.
# c_h is the curve height of the raphael curves.
# start_x is the leftmost side of the graph.
# y_topspace is the length, in pixels, of the space I've
#  allotted for all the shit that goes on top of the graph.
# RETURNS tuple (top raphael line, bottom raphael line)
def stringer(heights, width, spacing, c_h, start_x, y_topspace):
    # Add a curve to top and bottom raphael lines with specified
    #  change in x and y (y specified for top line)
    def curve(chx1, chy1, chx2, chy2, x, yt, yb, rt, rb):
        x += chx1
        yt += chy1
        yb -= chy1
        rt += 'S' + str(x) + ',' + str(yt) + ','
        rb += 'S' + str(x) + ',' + str(yb) + ','
        x += chx2
        yt += chy2
        yb -= chy2
        rt += str(x) + ',' + str(yt)
        rb += str(x) + ',' + str(yb)
        return [x, yt, yb, rt, rb]
    
    # Add a line to top and bottom raphael lines with specified
    #  change in x and y (y specified for top line)
    def line(chx, chy, x, yt, yb, rt, rb):
        x += chx
        yt += chy
        yb -= chy
        rt += 'L' + str(x) + ',' + str(yt)
        rb += 'L' + str(x) + ',' + str(yb)
        return [x, yt, yb, rt, rb]

    # Specify the y-coordinate from which to start.
    start_y = y_topspace + max(heights)/2 + c_h/2
    
    # Specify curve width of raphael curves.
    c_w = spacing
    
    # Start the raphael lines.
    rt = "M"+str(start_x)+"," + str(start_y) # raphael line top
    rb = "M"+str(start_x)+"," + str(start_y) # raphael line bottom
    
    # Initiate the x and y tracker variables.
    x = start_x
    yt =  start_y # y top
    yb =  start_y # y bottom

    diff = heights[0] / 2
    if diff <= (c_h/2):
    # vertical distance too short for connecting line
        [x, yt, yb, rt, rb] = curve(0, diff + (c_h/2), c_w, 0, x, yt, yb, rt, rb)
    else:
        [x, yt, yb, rt, rb] = line(0, diff - (c_h/2), x, yt, yb, rt, rb)
        [x, yt, yb, rt, rb] = curve(0, c_h, c_w, 0, x, yt, yb, rt, rb)
    [x, yt, yb, rt, rb] = line(width - c_w, 0, x, yt, yb, rt, rb)

    # Iterate through heights to draw top and bottom lines.
    for i in range(1, len(heights)):
        diff = (heights[i] - heights[i-1]) / 2
        if abs(diff) < 2*c_h:
            # vertical distance too short for connecting line
            rise = diff/2
            [x, yt, yb, rt, rb] = curve(c_w, 0, 0, rise, x, yt, yb, rt, rb)
            [x, yt, yb, rt, rb] =\
                curve( 0, diff - rise, c_w, 0, x, yt, yb, rt, rb)
        else:
            m = abs(diff)/diff # either 1 or -1 for rise or drop
            vdist = diff - m*20
            [x, yt, yb, rt, rb] = curve(c_w, 0, 0, m*c_h, x, yt, yb, rt, rb)
            [x, yt, yb, rt, rb] = line(0, vdist, x, yt, yb, rt, rb)
            [x, yt, yb, rt, rb] = curve(0, m*c_h, c_w, 0, x, yt, yb, rt, rb)
        [x, yt, yb, rt, rb] = line(width - c_w, 0, x, yt, yb, rt, rb)

    # Finish last piece of raphael lines
    diff = heights[-1] / 2
    extra = heights[-1] % 2
    if diff <= c_h / 2:
    # vertical distance too short for connecting line
        [x, yt, yb, rt, rb] = curve(c_w, 0, 0, -diff-extra, x, yt, yb, rt, rb)
        
    else:
        [x, yt, yb, rt, rb] = curve(c_w, 0, 0, -c_h, x, yt, yb, rt, rb)
        [x, yt, yb, rt, rb] = line(0, -diff+(c_h/2)-extra, x, yt, yb, rt, rb)
    return [rt, rb]

class WordCounter: # Looks for single words in article fulltexts
    def __init__(self, words, papa_dir, baby_dir y_topspace, c_h, div_width, div_spacing, s_f, start_x):
    # words is list of lower-case words to be searched for,
    # papa_dir is string of directory where the txt files to be searched are
    #   (sorted into sub-directory by year: each named "1987" through "2006")
    #   in which female obituaries are named by index: 0.txt, 1.txt, so on.
    # baby_dir is the directory to write results to.
    # y_topspace is the height, in pixels, allotted for all the stuff that goes
    #   above the raphael graph.
    # c_h is the curve height for the raphael graph.
    # div_width is the width of the sentence-holding divs on the graph.
    # div_spacing is the space between the sentence-holding divs.
    # s_f is the stretch factor with which to get div height from use rate.
    # start_x is the x-location, in pixels, where the raphael lines should start.
        self.papa_dir = papa_dir
        self.words = words
        self.baby_dir = baby_dir
        self.y_topspace = y_topspace
        self.c_h = c_h
        self.div_width = div_width
        self.div_spacing = div_spacing
        self.s_f = s_f
        self.start_x = start_x
        
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


    def generate_jsons(self):

        header_font_sizes = {word: 0 for word in self.words}

        heights_dict = {word:[] for word in self.words}

        rates_dict = {word:[] for word in self.words}

        content_dict = {word:[{'id': 'meta-data', \
                               'raphlines': [], \
                               'caption': '', \
                               'words_included': word, \
                               'max_height': 0, \
                               'c_h': self.c_h} for word in self.words]}

        for word in self.words:
            for i in range(20):
                content_dict[word].append(\
                    {'id': i, \
                     'sentences': [], \
                     'height': 0,
                     'rate': 0,
                     'sentence_index': 0})

        for year in range(1987, 2007):
            word_count = 0
            for article_index in range(self.yearly_female_obit_totals[year]):
                current_file = open(self.papa_dir+'/'+str(year)+'/'+str(article_index)+'.txt', 'r')
                fulltext = current_file.read()
                fulltext_cleaned = re.sub('        ', '', re.sub('\n', ' ', fulltext))
                tok_sent = [sentence for sentence in sent_tokenize(fulltext_cleaned)]
                tok_sent_clone = tok_sent[:]
                # Clean out duplicates
                for i in range(1, len(tok_sent)):
                    if tok_sent_clone[i] == tok_sent_clone[i-1]:
                        tok_sent.remove(tok_sent_clone[i])
                # Find word matches
                for sentence in tok_sent:
                    for word in word_tokenize(sentence):
                        word = word.lower()
                        if word in self.phrases:
                            word_count += 1
                            if sentence not in content_dict[word][year - 1986]['sentences']:
                                content_dict[word][year - 1986]['sentences'].append(sentence)

            # Calculate and store word-use-rates and related data
            for word in self.words:
                use_rate = \
                    (word_count/float(self.yearly_allword_totals[year]))*100000
                content_dict[word][year-1986]['rate'] = int(round(use_rate))
                height = int(round((use_rate*self.s_f)))-self.c_h
                content_dict[word][year-1986]['height'] = height
                heights_dict[word].append(height)
                rates_dict[word].append(use_rate)

        # Generate font sizes and raphael lines for each word.
        for word in self.words:
            avg_rate = int(round(sum(rates_dict[word]) / 20.0))
            font_size = 10 + min(avg_rate/20, 2)
            header_font_sizes[word] = font_size
            content_dict[word][0]['max_height'] = max(heights_dict[word])
            content_dict[word][0]['raphlines'] = stringer(heights_dict[word], self.div_width, \
                                                self.div_spacing, self.c_h, self.start_x, self.y_topspace)

        # Generate the jsons.

        topbar_datafile = open(baby_dir + '/topbar.json', 'w')
        content = [{'word': word, 'size': header_font_sizes[word]} for word in self.words]
        topbar_datafile.write(json.dumps(content, indent=4))
        topbar_datafile.close()
        for word in self.words:
            word_datafile = open(baby_dir + '/' + word + '.json', 'w')
            content = content_dict[word]
            word_datafile.write(json.dumps(content, indent=4))
            word_datafile.close()

if __name__ == "__main__":
    #__init__(self, words, papa_dir, baby_dir y_topspace, c_h, div_width, div_spacing, s_f, start_x):
    word_counter = WordCounter(["married", "founded", "research"], "obits_fem", "json_results", 200, 10, 40, 10, 3, 50)
    word_counter.generate_jsons()
