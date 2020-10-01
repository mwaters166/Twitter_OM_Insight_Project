'''
Script to scrape tweets using Tweepy
using tweet ids corresponding to 
specific dates. 

-Michele Waters
'''

from scrape_tweets_tweepy_functions import *
import sys
import csv

#Get input (twitter handles/user list of accounts) & output file (tweets)
input_users=sys.argv[1] #users.csv or users_test.csv (which is currently the default)
output_tweet_file=sys.argv[2] #tweets.csv

#Open file and extract relevant columns: product name, date received, and company name
def get_users(input_users):
    with open(input_users, encoding='utf-8-sig') as f: #users.csv
        input_file=csv.DictReader(f) #read columns
        user_list=[]
        for row in input_file:
            user=row['users'].lower()
            user_list.append(user)
    return user_list

users=get_users(input_users)

#User input Twitter developer keys and tokens to initialize api
#Note: do not include quotation marks around keys
tokens=get_api_tokens()

#Initialize Twitter api/Tweepy with keys and tokens
api=auth_api(tokens[0], tokens[1], tokens[2], tokens[3])

#Get date ranges to scrape
#Example entries: since_date: 9/1/2020 , until_date: 9/29/2020
date_range=get_date_ranges(time_id_file='time_ids.csv')

#Scrape and save tweets
scrape_and_save_tweets_from_user_list(api, user_list=users, output_file=output_tweet_file, since_id=date_range[0], until_id=date_range[1])

