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
from gensim.similarities import MatrixSimilarity, SparseMatrixSimilarity
from gensim.corpora.dictionary import Dictionary
import time
from scipy.spatial.distance import jensenshannon
import en_core_web_sm
nlp = en_core_web_sm.load()
import import_ipynb
import Dict_df_operations as dfo
import matplotlib.pyplot as plt
nltk_stopwords = stopwords.words("english")+["rt", "via","-»","--»","--","---","-->","<--","->","<-","«--","«","«-","»","«»"]


def get_lda_scores(data):
    path = input("Enter path to LDA model: ")
    lda = LdaModel.load(path+"lda_model")
    corpus = MmCorpus(path+"lda_corpus.mm")
    new_dictionary = Dictionary(data['tokens'])
    new_corpus = [new_dictionary.doc2bow(doc) for doc in data['tokens']]
    new_corpus = (lda[new_corpus][0])
    new_doc_distribution= []
    for i in range(len(new_corpus)):
        new_doc_distribution.append(new_corpus[i][1])
    new_doc_distribution = np.array(new_doc_distribution)
    
    doc_topic_dist = np.array([[tup[1] for tup in lst] for lst in lda[corpus]])
    doc_topic_dist.shape
    
    scores = []
    for i in range(len(doc_topic_dist)):
        scores.append(jensenshannon(new_doc_distribution,doc_topic_dist[i]))
    #data['scores'] = scores
    #similar = data.sort_values(by='scores', ascending=False)
    return scores

def predict_lda(new_data,original_data):
    scores = get_lda_scores(new_data)
    original_data['scores'] = scores
    similar = original_data['scores'].sort_values(ascending=False)
    return similar
    
def predict_tfid(pred_data,data):
    path = input("Enter path to LDA model: ")
    tfid = gensim.models.TfidfModel.load(path+"tfid_model")
    corpus = MmCorpus(path+"tfid_corpus.mm")
    tfid_corpus = tfid[corpus]
    new_dictionary = Dictionary(data['tokens'])
    new_corpus = [new_dictionary.doc2bow(doc) for doc in data['tokens']]
    index_sparse = SparseMatrixSimilarity(tfid_corpus, num_features=corpus.num_terms)
    index_sparse.num_best = 500
    idx =(index_sparse[new_corpus])
    print("Most Similar users are as follows: ")
    print("Name\t\t\tscore ")
    m=1
    for i in idx[0]:
        display("{}. {}     {}".format(m,data.iloc[i[0]]['handles'],i[1]))
        m+=1
    return


    