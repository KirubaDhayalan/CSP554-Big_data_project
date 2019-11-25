#!/usr/bin/env python
# coding: utf-8

# In[37]:


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
import pyLDAvis
import gensim 
from gensim.corpora import Dictionary, MmCorpus
from gensim.models import LdaModel
from gensim.models.wrappers import LdaMallet
from collections import Counter
from gensim.corpora.dictionary import Dictionary
import en_core_web_sm
import time
nlp = en_core_web_sm.load()
import import_ipynb
import Dict_df_operations as dfo
from scipy.stats import entropy
import matplotlib.pyplot as plt
nltk_stopwords = stopwords.words("english")+["rt", "via","-»","--»","--","---","-->","<--","->","<-","«--","«","«-","»","«»"]

def tokenizing(tweets):
    tokenized_tweets = []
    format_tweets = []
    lst = []
    for tweet in tweets:
        tokenized_tweet = nlp(tweet)
        tweet = ""
        for token in tokenized_tweet:
            #print(token.pos_)
            if token.pos_ in ['NOUN', 'PROPN', 'INTJ']:
                if token.is_space:
                    continue
                elif token.is_punct:
                    continue
                elif token.is_stop:
                    continue
                elif token.is_digit:
                    continue
                elif len(token) == 1:
                    continue
                elif len(token) == 2:
                    continue
                else:
                    tweet += str(token.lemma_) + " "
            else:
                continue
        tokenized_tweets.append(tweet)
    #print(tokenized_tweets)
    #tokenized_tweets = list(map(str.strip, tokenized_tweets)) 
    #tokenized_tweets = [x for x in tokenized_tweets if x != ""] 
    for tweet in tokenized_tweets:
        for split in tweet.split():
            lst.append(split)
        #format_tweets.append(lst)
    return lst

def group_tokens(df):
    tokens_lst = []
    tokenized_text = dict()
    handles  = df['handles']
    for i in range(len(handles)):
        print("Getting tokens! ",(len(handles)-i)," remaining....")
        tokens = (tokenizing(df.iloc[i]['text']))
        tokens_lst.append(tokens)
        #df.iloc[i]['tokenized_text'] = tokens
        df['tokens'] = list(tokens_lst)
        df.set_index('handles')
    return (df)


def get_tokens(dict):
    df = dfo.get_df(dict)
    df['handles'] = df.index
    display(df)
    df = dfo.filtration(df,'text')
    clean_df =  group_tokens(df)
    return clean_df
    

