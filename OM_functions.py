'''
Twitter Outrage Machine (OM)

Insight Data Science Project, Summer 2020

By Michele Waters

OM Functions for Streamlit Dashboard
'''


import pandas as pd
import requests
import numpy as np
import re
import string
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from spacy.lang.en import English
import nltk
from nltk.stem.snowball import SnowballStemmer
from nltk.stem import WordNetLemmatizer 
nltk.download('wordnet')
from sklearn.linear_model import LogisticRegression
import pickle
import streamlit as st
#import gensim.downloader as api
#glove_twitter = api.load("glove-twitter-200") #Uncomment if desire to replace below glove_twitter variable (with unique training vectors) with all vectors in stanford GloVe library-- but this is much slower to load
unique_glove_file = open("unique_glove_vectors.pkl", "rb")
glove_twitter = pickle.load(unique_glove_file)


class Tweet():
    #Initialize Tweet class with tweet text and Twitter user name
    def __init__(self, tweet_text, user_name):
        self.tweet_text=tweet_text
        self.user_name=user_name
    #Function to get follower account
    def get_followers(self):
        url='https://cdn.syndication.twimg.com/widgets/followbutton/info.json?screen_names='+self.user_name
        response=requests.get(url).json()
        followers_count=response[0]['followers_count']
        return followers_count
    #Remove contractions
    def clean_contractions(self):
        contraction_list = { 
        "ain’t": "am not",
        "aren’t": "are not",
        "can’t": "cannot",
        "can’t’ve": "cannot have",
        "’cause": "because",
        "could’ve": "could have",
        "couldn’t": "could not",
        "couldn’t've": "could not have",
        "didn’t": "did not",
        "doesn’t": "does not",
        "don’t": "do not",
        "’em": "them",
        "hadn’t": "had not",
        "hadn’t've": "had not have",
        "hasn’t": "has not",
        "haven’t": "have not",
        "he’d": "he would",
        "he’d’ve": "he would have",
        "he’ll": "he will",
        "here’s": "here is",
        "he’s": "he is",
        "how’d": "how did",
        "how’ll": "how will",
        "how’s": "how is",
        "i’d": "i would",
        "i’ll": "i will",
        "i’m": "i am",
        "i’ve": "i have",
        "isn’t": "is not",
        "it’d": "it would",
        "it’ll": "it will",
        "it’s": "it is",
        "let’s": "let us",
        "ma’am": "madam",
        "mayn’t": "may not",
        "might’ve": "might have",
        "mightn’t": "might not",
        "must’ve": "must have",
        "mustn’t": "must not",
        "needn’t": "need not",
        "oughtn’t": "ought not",
        "shan’t": "shall not",
        "sha’n’t": "shall not",
        "she’d": "she would",
        "she’ll": "she will",
        "she’s": "she is",
        "should’ve": "should have",
        "shouldn’t": "should not",
        "that’d": "that would",
        "that’s": "that is",
        "there’d": "there had",
        "there’s": "there is",
        "they’d": "they would",
        "they’ll": "they will",
        "they’re": "they are",
        "they’ve": "they have",
        "wasn’t": "was not",
        "we’d": "we would",
        "we’ll": "we will",
        "we’re": "we are",
        "we’ve": "we have",
        "weren’t": "were not",
        "what’ll": "what will",
        "what’re": "what are",
        "what’s": "what is",
        "what’ve": "what have",
        "where’d": "where did",
        "where’s": "where is",
        "who’ll": "who will",
        "who’s": "who is",
        "won’t": "will not",
        "wouldn’t": "would not",
        "you’d": "you would",
        "you’ll": "you will",
        "you’re": "you are",
        "thx"   : "thanks"
        }
        sentence=""
        for word in self.tweet_text.lower().replace('"', '').replace("'", '’').split():
            if word in contraction_list.keys():
                sentence+=f" {contraction_list[word]}"
            else:
                sentence+=f" {word}"
        return sentence
    # Function to remove stopwords/Tokenize data/remove punctuation
    def spacy_tokenizer(self):
        punctuations = string.punctuation # Create our list of punctuation marks
        nlp = spacy.load('en') #Load spacy
        stop_words = spacy.lang.en.stop_words.STOP_WORDS # Create our list of stopwords
        parser = English() # Load English tokenizer, tagger, parser, NER and word vectors
        # Creating our token object, which is used to create documents with linguistic annotations.
        mytokens = parser(self.clean_contractions()) 
        # Lemmatizing each token and converting each token into lowercase
        mytokens = [ word.lemma_.lower().strip() if word.lemma_ != "-PRON-" else word.lower_ for word in mytokens ]
        # Removing stop words, list of tokens
        mytokens = [ word for word in mytokens if word not in stop_words and word not in punctuations ]
        return mytokens
    # Function to return tokenized word list as list of sentences
    def assemble_tokenized_tweet(self, token_tweet_list):
        token_sentences=[]
        for token_tweet in token_tweet_list:
            token_sentences.append(' '.join(token_tweet))
        return token_sentences
    #Function to remove punctuation not removed by spacy tokenizer function
    def remove_punctuation(self, token_tweet_list):
        token_sentences=[]
        for token_tweet in token_tweet_list:
            token_sentences.append(re.sub(r'[^a-zA-Z\s]', ' ', token_tweet.replace('.', ' ')).replace('\s+\s', ' '))
        return token_sentences
    #Function to stem words in sentences
    def stem_sentences(self, token_tweet_list):
        stemmer = SnowballStemmer(language='english')
        stem_token_sentences=[]
        for token_tweet in token_tweet_list:
            stem_tokens=[]
            for token in token_tweet:
                stem_tokens.append(stemmer.stem(token))
            stem_token_sentences.append(' '.join(stem_tokens))
        return stem_token_sentences
    @st.cache 
    def lemmatize_sentences(self, token_sentences):
        lemmatizer = WordNetLemmatizer() 
        lm_sentences=[]
        for token_sentence in token_sentences:
            lm_sentence=[]
            for word in token_sentence.split():
                lm_sentence.append(lemmatizer.lemmatize(word))
            lm_sentences.append(' '.join(lm_sentence))
        return lm_sentences

#Function to transform tweet to GloVe vector
def word_to_glove_vector(tweet, size, vectors, aggregation='mean'):
    vec = np.zeros(size).reshape((1, size))
    count = 0.
    for word in tweet.split():
        try:
            vec += np.array(vectors[word]).reshape((1, size))
            count += 1.
        except KeyError:
            continue
    if aggregation == 'mean':
        if count != 0:
            vec /= count
        return vec
    elif aggregation == 'sum':
        return vec

#Function to return scaled GloVe vector, based on training data   
def glove_scaler(text):
    # load the GloVe text scaler from disk
    glove_scaler_file = 'glove_scaler.sav'
    load_scaler= pickle.load(open(glove_scaler_file, 'rb'))
    vector = load_scaler.transform(np.concatenate([word_to_glove_vector(tweet, 200, glove_twitter,'mean') for tweet in text]))
    return vector

#Function to predict probability of being ratioed, using GloVE + Logistic Regression
def add_resid_predictions(account_rf,account_val, clf, vector_X, threshold=0.5):
    resid_prob_val=account_rf.predict(account_val)
    new_prob=[val[1] for val in clf.predict_proba(vector_X)]+resid_prob_val
    new_prob=pd.Series(new_prob).apply(lambda x: x if x>=0 else 0)
    percent_prob= [round(num*100, 2) for num in new_prob]
    pred_new_prob=[]
    for num in new_prob:
        if num>=threshold: #threshold; default, predict 1 if threshold is over 0.5, 0 if less than 0.5
            pred_new_prob.append(1)
        else:
            pred_new_prob.append(0)
    return [percent_prob, pred_new_prob]

#Function to return ratio detector message
def run_ratio_detector(percent_prob):
    if percent_prob>=50.0:
        if percent_prob>100:
            percent_prob=100
        st.write(f"RATIO DETECTED! You have a {percent_prob}% chance of being ratioed and inciting outrage. Are you sure you'd like to send that tweet?")
    else:
        if percent_prob<0:
            percent_prob=0
        st.write(f"Ratio Not Detected. You have a {percent_prob}% chance of being ratioed. You're ready to tweet!")


