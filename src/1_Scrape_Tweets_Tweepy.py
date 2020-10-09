'''
Script to scrape tweets using Tweepy
using tweet ids corresponding to 
specific dates.

(Python)

-Michele Waters
'''

from scrape_tweets_tweepy_functions import *
import sys

#Get input (twitter handles/user list of accounts) & output file (tweets)
input_users=sys.argv[1] #users.csv or users_test.csv (which is currently the default)
output_tweet_file=sys.argv[2] #tweets.csv

#Open file and extract relevant columns: product name, date received, and company name
users=get_users(input_users)

#User input Twitter developer keys and tokens to initialize api
#Note: do not include quotation marks around keys
tokens=get_api_tokens()

#Initialize Twitter api/Tweepy with keys and tokens
api=auth_api(tokens[0], tokens[1], tokens[2], tokens[3])

#Get date ranges to scrape
#Example entries: since_date: 9/1/2020 , until_date: 9/29/2020
date_range=check_date_validity()

#Scrape and save tweets
scrape_and_save_tweets_from_user_list(api, user_list=users, output_file=output_tweet_file, since_id=date_range[0], until_id=date_range[1])

