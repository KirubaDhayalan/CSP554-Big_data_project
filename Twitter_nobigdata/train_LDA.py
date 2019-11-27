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
import gensim 
from gensim.corpora import Dictionary, MmCorpus
from gensim.models import LdaModel
from gensim.models.coherencemodel import CoherenceModel
from collections import Counter
from gensim.corpora.dictionary import Dictionary
import en_core_web_sm
import time
nlp = en_core_web_sm.load()
#import import_ipynb
import dict_df_helper as dfo
from scipy.stats import entropy
import matplotlib.pyplot as plt
nltk_stopwords = stopwords.words("english")+["rt", "via","-»","--»","--","---","-->","<--","->","<-","«--","«","«-","»","«»"]

def train_lda(data , num_topics):
    chunksize = 300
    dictionary = Dictionary(data['tokens'])
    corpus = [dictionary.doc2bow(doc) for doc in data['tokens']]
    t1 = time.time()
    # low alpha means each document is only represented by a small number of topics, and vice versa
    # low eta means each topic is only represented by a small number of words, and vice versa
    lda = LdaModel(corpus=corpus, num_topics=num_topics, id2word=dictionary,
                   alpha=0.1, eta=0.001, chunksize=chunksize, minimum_probability=0.0, passes=2)
    t2 = time.time()
    print("Time to train LDA model on ", len(data), "articles: ", (t2-t1)/60, "min")
    return dictionary,corpus,lda

def coherence_analysis(data,step=1):
    coherence_values = []
    model_list = []
    for num_topics in range(5, 100,step):
        print("Getting coherence value for {} topics".format(num_topics))
        dict, corpus , model= train_lda(data,num_topics)
        model_list.append(model)
        coherencemodel = CoherenceModel(model=model, texts=data['tokens'], dictionary=dict, coherence='c_v')
        coherence_values.append(coherencemodel.get_coherence())
    x = range(5, 100)
    print("Topics with max Coherence is {}".format(np.argmax(coherence_values)))
    plt.plot(x, coherence_values)
    plt.xlabel("Num Topics")
    plt.ylabel("Coherence score")
    plt.legend(("coherence_values"), loc='best')
    plt.show()
    return max(coherence_values)

def explore_topic(model, topic_number, topn=15):
    """
    accept a user-supplied topic number and
    print out a formatted list of the top terms
    """
        
    print (u'{:20} {}'.format(u'term', u'frequency') + u'\n')

    for term, frequency in model.show_topic(topic_number, topn=topn):
        print( u'{:20} {:.3f}'.format(term, round(frequency, 3)))

def coherence_score(model,tokens_lst,dictionary):
    coherence_model_lda = CoherenceModel(model=model, texts=data['tokens'], dictionary=dictionary, coherence='c_v')
    coherence_lda = coherence_model_lda.get_coherence()
    print('\nCoherence Score: ', coherence_lda)
    
def lda_save(lda,corpus):
    path = input("Enter path to save the lda model: ")
    lda.save(str(path+"{}".format('lda_model')))
    MmCorpus.serialize(path+"{}.mm".format("lda_corpus"), corpus)