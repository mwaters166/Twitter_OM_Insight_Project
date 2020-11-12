'''
Functions to scrape tweets using Tweepy
using tweet ids corresponding to 
specific dates.

(Python)

-Michele Waters
'''

import pandas as pd
import tweepy
from Twitter_User_class import Twitter_User
from Tweet_Builder_class import Tweet_Builder
    
def get_tweepy_date_id(loaded_time_df, date='2/1/2020'):
    '''
    Function to return tweet id from given date
    '''
    time_dict={record['date']:record['id'] for record in loaded_time_df.to_dict('records')}
    if date in time_dict:
        return time_dict[date]
    else:
        return 'Date not present; choose a different date'
    
def get_date_range():
    '''
    Get date ranges from user, valid dates range from 1/1/2020 to 9/29/2020; but some dates are missing.
    Check time_ids.csv for all available dates.
    '''
    since_date=input("Enter start date for scraping (e.g. 9/1/2020): ")
    until_date=input("Enter end date for scraping (e.g. 9/29/2020): ")
    return [since_date, until_date]

def get_date_id(date, loaded_time_df):
    '''
    Function to get time id from date
    '''
    time_id=get_tweepy_date_id(loaded_time_df, date)
    if type(time_id) is int:
        return [True, time_id]
    else:
        return [False, 'Try a different date, from 1/1/2020-9/29/2020']
    
def check_date_validity(loaded_time_df, since_valid=False, until_valid=False):
    '''
    Function to check if date ranges are valid. While either date validity is False, will request
    the user to enter a different date. Valid dates are present in time_ids.csv
    '''
    while since_valid is False or until_valid is False:
        since_date, until_date=get_date_range() #Get dates
        since_valid, since_id=get_date_id(since_date, loaded_time_df) #Get date validity and date id for date #1
        until_valid, until_id=get_date_id(until_date, loaded_time_df) #Get date validity and date id for date #2
        print(f'Date #1 valid?: {since_valid}-->{since_date}: {since_id}; Date #2 valid?: {until_valid}-->{until_date}: {until_id}')
    return [since_id, until_id]
                         
def scrape_user_tweets(api, user, since_id, until_id):
    '''
    Function to scrape and return dataframe of tweets for individual users
    '''
    tweets=Tweet_Builder(api, user)
    tweet_df=tweets.get_user_tweets(since_id=since_id, max_id=until_id)
    return tweet_df

def select_tweet_attributes(attributes=['created_at','id','full_text','entities','in_reply_to_status_id',
                           'in_reply_to_user_id','in_reply_to_screen_name','user',
                           'is_quote_status', 'retweet_count','favorite_count',
                           'favorited','retweeted','lang']):
    return attributes

def get_select_tweet_df(tweet_df, select_tweet_info):
    return tweet_df[select_tweet_attributes(select_tweet_info)]

def save_tweets_from_users(select_tweet_df, output_file, user):
    select_tweet_df.to_csv(output_file, mode='a', header=False, index=None)
    print(f'{user} saved!')

def run_scrape_save(api, users, output_file, select_tweet_info, since_id, until_id):
    '''
    Function to scrape and save tweets in csv files given a list of users
    '''
    pd.DataFrame(columns=select_tweet_info).to_csv(output_file, index=None)
    for user in users:
        tweet_df=scrape_user_tweets(api, user, since_id, until_id) #Scrape tweets
        if tweet_df.empty: continue #skips user if tweets not present in specified date range
        select_tweet_df=get_select_tweet_df(tweet_df, select_tweet_info) #select attributes
        save_tweets_from_users(select_tweet_df, output_file, user) #save selected tweet dataframe to output file
    
