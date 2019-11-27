import pickle
import nltk
import pandas as pd
import numpy as np
import tweepy
import re
import json
from tweepy.models import Status
import pandas as pd
import string
from nltk.corpus import stopwords
import spacy
#import pyLDAvis
import gensim 
from gensim.models import Phrases
from gensim.models.word2vec import LineSentence
from gensim.corpora import Dictionary, MmCorpus
from gensim.models import LdaModel
#from gensim.models.wrappers import LdaMallet
from collections import Counter
from gensim.corpora.dictionary import Dictionary
import time
import en_core_web_sm
nlp = en_core_web_sm.load()
#import import_ipynb
import dict_df_helper as dfo
import matplotlib.pyplot as plt
nltk_stopwords = stopwords.words("english")+["rt", "via","-»","--»","--","---","-->","<--","->","<-","«--","«","«-","»","«»"]


def train_tfid(data):
    dictionary = Dictionary(data['tokens'])
    corpus = [dictionary.doc2bow(doc) for doc in data['tokens']]
    t1 = time.time()
    tfidf_model = gensim.models.TfidfModel(corpus, id2word=dictionary)
    tfid_corpus = tfidf_model[corpus]
    return tfidf_model, tfid_corpus

def tfid_save(tfid,corpus):
    path = input("Enter path to save the tfid model: ")
    tfid.save(str(path+"{}".format('tfid_model')))
    MmCorpus.serialize(path+"{}.mm".format("tfid_corpus"), corpus)