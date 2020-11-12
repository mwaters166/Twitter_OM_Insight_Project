import tweepy
import os
from dotenv import load_dotenv
load_dotenv(verbose=True)  # Throws error if it can't find .env file

class Tweepy_Client():
    '''
    Creation of Tweepy client class. Gets Twitter developer keys and tokens to initialize api from '.env' file 
    defined by user. Initializes Twitter api/Tweepy with keys and tokens
    '''
    api_key = os.getenv("api_key")
    api_secret_key = os.getenv("api_secret_key")
    access_token=os.getenv("access_token")
    access_token_secret=os.getenv("access_token_secret")
    
    def __init__(self):
        auth = tweepy.OAuthHandler(self.api_key, self.api_secret_key)
        auth.set_access_token(self.access_token, self.access_token_secret)
        self.api = tweepy.API(auth, wait_on_rate_limit=True) 
