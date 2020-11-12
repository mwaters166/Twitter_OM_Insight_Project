'''
Script to scrape tweets using Tweepy
using tweet ids corresponding to 
specific dates.

(Python)

-Michele Waters
'''

from scrape_tweets_tweepy_functions import *
from Tweepy_Client_class import Tweepy_Client
import sys
import pandas as pd

#Get input (twitter handles/user list of accounts) & output file (tweets)
input_users=sys.argv[1] #users.csv or users_test.csv (which is currently the default)
output_tweet_file=sys.argv[2] #tweets.csv

#Get list of user names from input file
users=list(pd.read_csv(input_users).users)

#Create Tweepy_Client class 
client=Tweepy_Client()

#Import date ids as dataframe
loaded_time_df=pd.read_csv('./time_id_data/time_ids.csv', index_col=0)

#Get date ranges to scrape; Example entries: since_date: 9/1/2020 , until_date: 9/29/2020
date_range=check_date_validity(loaded_time_df)

#Select tweet attributes 
select_tweet_info=select_tweet_attributes() # list of tweet attributes ['created_at','id','full_text', ...]

#Scrape and save tweets
run_scrape_save(api=client.api, users=users, output_file=output_tweet_file, select_tweet_info=select_tweet_info, since_id=date_range[0], until_id=date_range[1])

