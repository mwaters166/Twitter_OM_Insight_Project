import streamlit as st

from PIL import Image
image = Image.open('twit_pic.png')

st.image(image, caption=None, use_column_width=True)

st.subheader('Insight Project by Michele Waters')


user_screename = st.text_input("Input Twitter handle:", "elonmusk")

user_input = st.text_input("Input tweet to determine ratio probability:", "I hate puppies!")

model_output=0.96

if st.button('Run Ratio Detector!'):
    if model_output>=0.5:
        st.write(f"You have a {model_output*100}% chance of being ratioed and inciting outrage. Are you sure you'd like to send that tweet?")
    else:
        st.write(f"You have a {model_output*100}% chance of being ratioed and inciting outrage. Ready to send!")

