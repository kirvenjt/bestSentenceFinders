import nltk
import string
import os
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer
import scipy.sparse as sps

import nltk.data

import matplotlib.pyplot
from matplotlib.widgets import Slider
import pylab
import mpld3
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

path = '/Users/tuckerkirven/Desktop/Independent Study/levelDesign1.txt'
token_dict = {}
token_dict2= {}
sentence_list = []
stemmer = PorterStemmer()

def stem_tokens(tokens, stemmer):
    stemmed = []
    for item in tokens:
        stemmed.append(stemmer.stem(item))
    return stemmed

def tokenize(text):
    tokens = nltk.word_tokenize(text)
    stems = stem_tokens(tokens, stemmer)
    return stems


file_path = path
shakes = open(file_path, 'r')
text = shakes.read()
text = re.sub('[^\x00-\x7F]+',' ', text)
sentences = tokenizer.tokenize(text)
lowers = text.lower()
no_punctuation = lowers.translate(None, string.punctuation)
#token_dict[file] = no_punctuation
        
#this can take some time


maxNum = 0
maxSent =""
sentence_list.append((sentences[0], sps.coo_matrix(([0], ([0], [0])), shape=(1, 1))))
for i in xrange(1,len(sentences) -1):
    textSoFar = " ".join(sentences[:i])
    
    lowers = textSoFar.lower()
    no_punctuation = lowers.translate(None, string.punctuation)
    token_dict[file] = no_punctuation
    tfidf = TfidfVectorizer(tokenizer=tokenize, stop_words='english')
    tfs = tfidf.fit_transform(token_dict.values())

    curSent = sentences[i]
    lowers = curSent.lower()
    no_punctuation = lowers.translate(None, string.punctuation)
    tfs2 = tfidf.transform([no_punctuation])

    val = tfs2*tfs.T
    sentence_list.append((curSent, val))
    
x = []
y = []

count = 0
for key, value in sentence_list:

    x.append(count)
    y.append(value.data)
    print value.data
    count+=1

axframe = matplotlib.pyplot.axes([0.0, 0.1, 1, 0.05])

parRanges = [3,13,19,25,31,41,46,55,63,81,85,100,109,115,124,133,137,142,151,154,159,162,165,172,175,180,188,192,196]
last = -1
c = 0
for par in parRanges:
    if c % 2 ==0:
        matplotlib.pyplot.axvspan(last+.2, par+.2, facecolor='b', alpha=0.5)
    last = par
    c+=1

matplotlib.pyplot.axis([-1, 200, 0, 1]) # Put in side your range [xmin,xmax,ymin,ymax], like ax.axis([-5,5,-5,200])
#matplotlib.pyplot.xlim([0,200])
bestParSents = [1, 5, 18, 24, 29, 40, 43, 49, 56, 69, 85, 94, 101, 115, 118, 129, 136, 142, 145, 152, 157, 160, 164, 166, 174, 180, 186, 190, 196]
bestOveralSents = [97, 167, 81, 116, 80, 127, 0, 182, 102, 66, 193, 136, 166, 85, 31, 101, 145, 96, 26, 86, 29, 196, 25, 134, 186, 183, 30, 188, 143]
z = []
for a in x:
    if a in bestOveralSents:
        z.append('r')
    else:
        z.append('b')
matplotlib.pyplot.locator_params(nbins=64)
matplotlib.pyplot.scatter(x,y,c=z)

matplotlib.pyplot.show()


