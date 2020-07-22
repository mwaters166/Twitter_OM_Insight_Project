'''
Twitter Outrage Machine (OM)

Insight Data Science Project, Summer 2020

By Michele Waters

Streamlit Dashboard
'''


import streamlit as st
import pandas
import time

#Display header image
from PIL import Image
image = Image.open('twit_pic.png')

st.image(image, caption=None, use_column_width=True)

#Header
st.header('Insight Project by Michele Waters')

with st.spinner('Loading Outrage Machine...'):
    time.sleep(5)
from OM_functions import *
st.success('The Outrage Machine is Ready!')

st.subheader("User Name:")
#Get Twitter user name
user_name = st.text_input('Input Twitter handle:', 'cillizzacnn')

st.subheader("Tweet Text:")
#Get tweet text 
tweet_text = st.text_input("Input tweet to determine ratio probability:", "I love cnn!!")

st.write("In the example tweet above, try changing the word 'love' to 'hate' to see a different result!")

#Initialize Tweet class with text and username
tweet=Tweet(tweet_text, user_name)

#Get user number of followers
follower_count=tweet.get_followers()
#st.write(f'Number of followers is: {follower_count}')

#Load scaler for follower count, based on training data 
load_follower_scaler= pickle.load(open('follower_scaler.sav', 'rb'))
scaled_follower_count=load_follower_scaler.transform(pd.DataFrame([follower_count]))

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
#st.write(lem_tweet)

#Convert cleaned tweet to GloVe vector
tweet_vector=glove_scaler(lem_tweet)
#st.table(tweet_vector)

# Load the GloVe text + Logistic Regression model 
load_glove_clf= pickle.load(open('glove_clf.sav', 'rb'))

# Load the Number of Followers Random Forest model to calculate residual/error 
load_follower_rf= pickle.load(open('follower_rf.sav', 'rb'))

#Ratio Predictions & Classifications using Logistic Regression (GloVe embedded text) + Random Forest (residual prediction)
results=add_resid_predictions(account_rf=load_follower_rf,account_val=scaled_follower_count, clf=load_glove_clf, vector_X=tweet_vector, threshold=0.5)

percent_prob=results[0][0] #percent probability of being ratioed

class_pred=results[1][0] #classification/predictions (ratio/non-ratio)

st.subheader("Ratio Detector:")
#Ratio Detector Button
st.write("Click me:")
if st.button('Run Ratio Detector!'):
    ratio_detector= run_ratio_detector(percent_prob)
