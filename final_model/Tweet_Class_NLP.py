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
import json 

class Tweet():
    def __init__(self, tweet_text, user_name):
        '''Initialize Tweet class with tweet text and Twitter user name'''
        self.tweet_text=tweet_text
        self.user_name=user_name
    def get_followers(self):
        '''Get follower count'''
        url='https://cdn.syndication.twimg.com/widgets/followbutton/info.json?screen_names='+self.user_name
        response=requests.get(url).json()
        followers_count=response[0]['followers_count']
        return followers_count
    def clean_contractions(self):
        '''Remove contractions'''
        with open('contractions.txt', 'rb') as contraction_data: 
            contractions = contraction_data.read() 
        contraction_dict = json.loads(contractions)  
        sentence=""
        for word in self.tweet_text.lower().replace('"', '').replace("'", '’').split():
            if word in contraction_dict.keys():
                sentence+=f" {contraction_dict[word]}"
            else:
                sentence+=f" {word}"
        return sentence
    def spacy_tokenizer(self):
        '''Remove stopwords/Tokenize data/remove punctuation'''
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
    def assemble_tokenized_tweet(self, token_tweet_list):
        '''Return tokenized word list as list of sentences'''
        token_sentences=[]
        for token_tweet in token_tweet_list:
            token_sentences.append(' '.join(token_tweet))
        return token_sentences
    def remove_punctuation(self, token_tweet_list):
        '''Remove punctuation not removed by spacy tokenizer function'''
        token_sentences=[]
        for token_tweet in token_tweet_list:
            token_sentences.append(re.sub(r'[^a-zA-Z\s]', ' ', token_tweet.replace('.', ' ')).replace('\s+\s', ' '))
        return token_sentences
    def stem_sentences(self, token_tweet_list):
        '''Stem words in sentences'''
        stemmer = SnowballStemmer(language='english')
        stem_token_sentences=[]
        for token_tweet in token_tweet_list:
            stem_tokens=[]
            for token in token_tweet:
                stem_tokens.append(stemmer.stem(token))
            stem_token_sentences.append(' '.join(stem_tokens))
        return stem_token_sentences
    def lemmatize_sentences(self, token_sentences):
        '''Lemmatize words in sentences'''
        lemmatizer = WordNetLemmatizer() 
        lm_sentences=[]
        for token_sentence in token_sentences:
            lm_sentence=[]
            for word in token_sentence.split():
                lm_sentence.append(lemmatizer.lemmatize(word))
            lm_sentences.append(' '.join(lm_sentence))
        return lm_sentences