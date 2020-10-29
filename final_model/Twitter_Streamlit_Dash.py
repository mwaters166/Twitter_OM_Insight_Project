'''
Twitter Outrage Machine (OM)

Insight Data Science Project, Summer 2020

By Michele Waters

Streamlit Dashboard
'''
import streamlit as st
import time
from PIL import Image
from OM_functions import *

st.image(Image.open('../images/twit_pic.png'), caption=None, use_column_width=True) #Display header image

st.header('Insight Project by Michele Waters') #Header

st.subheader("User Name:")

user_name = st.text_input('Input Twitter handle:', 'cillizzacnn') #Get Twitter user name

st.subheader("Tweet Text:")

tweet_text = st.text_input("Input tweet to determine ratio probability:", "I love cnn!!") #Get tweet text 

st.write("In the example tweet above, try changing the word 'love' to 'hate' to see a different result!")

#Run model: Return percent probability of being ratioed & classification/predictions (ratio/non-ratio)
percent_prob, class_pred= run_model(tweet_text, user_name)

with st.spinner('Loading Outrage Machine...'): #Loading message
    time.sleep(5)

st.success('The Outrage Machine is Ready!')

st.subheader("Ratio Detector:")

#Ratio Detector Button
st.write("Click me:")
if st.button('Run Ratio Detector!'):
    ratio_class, ratio_detector= run_ratio_detector(percent_prob)
    if ratio_class=='ratio':
        st.write(f"RATIO DETECTED! You have a {percent_prob}% chance of being ratioed and inciting outrage. Are you sure you'd like to send that tweet?")
    else:
        st.write(f"Ratio Not Detected. You have a {percent_prob}% chance of being ratioed. You're ready to tweet!")
