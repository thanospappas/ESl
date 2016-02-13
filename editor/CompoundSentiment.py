from nltk import tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.util import *

class CompoundSentiment:

    def computeVaderScore(self,sentence):
        sid = SentimentIntensityAnalyzer()
        ss = sid.polarity_scores(sentence)
        retList = []
        for k in sorted(ss):
            retList.append(ss[k])

        return retList

