'''
Twitter Outrage Machine (OM)

Insight Data Science Project, Summer 2020

By Michele Waters

Functions to vectorize tweet and run model for Streamlit Dashboard
'''

import pandas as pd
import numpy as np
import pickle
from Tweet_Class_NLP import Tweet

def text_processing(tweet):
    #Clean contractions and get tokenized word list using spacy
    tokenized_word_list=tweet.spacy_tokenizer()
    #Assemble tokenized tweet
    tokenized_tweet=tweet.assemble_tokenized_tweet([tokenized_word_list])
    #Second pass, remove punctuation
    cleaned_tweet=tweet.remove_punctuation(tokenized_tweet)
    # #Stemmed tweet
    # stem_tweet=tweet.stem_sentences([cleaned_tweet])
    #Lemmatize tweet
    lem_tweet=tweet.lemmatize_sentences(cleaned_tweet)
    return lem_tweet

def word_to_glove_vector(tweet, size, vectors, aggregation='mean'):
    '''
    Transform tweet to GloVe vector
    '''
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
    
def glove_scaler(text, glove_vector_file='unique_glove_vectors.pkl', glove_scaler_file='glove_scaler.sav'):
    '''
    Return scaled GloVe vector, based on training data 
    '''
    glove_twitter = pickle.load(open(glove_vector_file, "rb")) #Load unique GloVe vectors
    load_scaler= pickle.load(open(glove_scaler_file, 'rb')) # load the GloVe text scaler from disk
    vector = load_scaler.transform(np.concatenate([word_to_glove_vector(tweet, 200, glove_twitter,'mean') for tweet in text]))
    return vector

def load_models(glove_lr_classifer='glove_clf.sav', rf_error='follower_rf.sav'):
    '''Load the GloVe text + Logistic Regression model & load the Number of Followers Random Forest model to calculate residual/error 
    '''
    load_glove_clf= pickle.load(open(glove_lr_classifer, 'rb'))
    load_follower_rf= pickle.load(open(rf_error, 'rb'))
    return [load_glove_clf, load_follower_rf]
    
def scale_followers(tweet, scaler='follower_scaler.sav'):
    follower_count=tweet.get_followers() #Get user number of followers
    #Load scaler for follower count, based on training data 
    load_follower_scaler= pickle.load(open(scaler, 'rb'))
    scaled_follower_count=load_follower_scaler.transform(pd.DataFrame([follower_count]))
    return scaled_follower_count

def add_resid_predictions(account_rf,account_val, clf, vector_X, threshold=0.5):
    '''
    Predict probability of being ratioed, using GloVE + Logistic Regression, with residuals predicted by Random Forest
    '''
    resid_prob_val=account_rf.predict(account_val) #residuals predicted by Random Forest
    new_prob=[val[1] for val in clf.predict_proba(vector_X)]+resid_prob_val #predicted probability from GloVe Logistic Regression added to RF residuals
    new_prob=pd.Series(new_prob).apply(lambda x: x if x>=0 else 0)
    percent_prob= [round(num*100, 2) for num in new_prob]
    pred_new_prob=[]
    for num in new_prob:
        if num>=threshold: #threshold; default, predict 1 if threshold is over 0.5, 0 if less than 0.5
            pred_new_prob.append(1)
        else:
            pred_new_prob.append(0)
    return [percent_prob, pred_new_prob]

def run_model(tweet_text, user_name):
    '''Run model: Return percent probability of being ratioed & classification/predictions (ratio/non-ratio)
    '''
    tweet=Tweet(tweet_text, user_name)  #Initialize Tweet class with text and username
    lem_tweet=text_processing(tweet) #Clean contractions, remove punctuation, lemmatize tweet
    tweet_vector=glove_scaler(lem_tweet) #Convert cleaned tweet to GloVe vector
    load_glove_clf, load_follower_rf=load_models() #Load Glove-Logistic Regression/ Random Forest error models
    scaled_follower_count=scale_followers(tweet) #Get scaled follower count
    results=add_resid_predictions(account_rf=load_follower_rf,account_val=scaled_follower_count, clf=load_glove_clf, vector_X=tweet_vector, threshold=0.5) #Ratio Predictions & Classifications
    percent_prob, class_pred=results[0][0], results[1][0]
    return [percent_prob, class_pred]
    
def run_ratio_detector(percent_prob):
    '''
    Determine whether tweet should be classified as ratio; set probabilities over/under 100/0 (after RF residual adjustment) to 100/0 respectively
    '''
    if percent_prob>=50.0:
        if percent_prob>100:
            percent_prob=100
        return ['ratio', percent_prob]
    else:
        if percent_prob<0:
            percent_prob=0
        return ['non_ratio', percent_prob]
    