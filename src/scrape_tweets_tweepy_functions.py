'''
Functions to scrape tweets using Tweepy
using tweet ids corresponding to 
specific dates.

(Python)

-Michele Waters
'''

import pandas as pd
import tweepy

def get_users(file_name):
    '''
    Get twitter handles/user names of accounts to scrape
    '''
    users=list(pd.read_csv(file_name).users)
    return users

def get_api_tokens():
    '''
    Get twitter developer keys and tokens
    '''
    api_key=input('Enter api_key: ')
    api_secret_key=input('api_secret_key: ')
    access_token=input('access_token: ')
    access_token_secret=input('access_token_secret: ')
    return [api_key, api_secret_key, access_token, access_token_secret]

def auth_api(api_key, api_secret_key, access_token, access_token_secret):
    '''
    Function to authorize api with keys and tokens
    '''
    auth = tweepy.OAuthHandler(api_key, api_secret_key)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True) 
    return api

class Tweepy_User():
    '''
    Creation of Tweepy class, initialized by api auth and twitter user name/twitter handle
    '''
    def __init__(self, api, user_name):
        self.api=api
        self.user=api.get_user(user_name)
        self.id=self.user.id
        self.follower_num=self.user.followers_count
        self.friend_num=self.user.friends_count
        
    def get_user_info_df(self, result='dictionary'):
        '''
        Gets user account information, returning select attributes
        '''
        select_attributes=['screen_name','name','id', 'profile_location', 'description',\
                           'protected','followers_count', 'friends_count', 'listed_count', \
                           'created_at','profile_image_url','favourites_count','verified', \
                           'statuses_count','lang']
        select_info_dict={k:v for k, v in self.user._json.items() if k in select_attributes}
        if result=='df':
            select_info_dict=pd.DataFrame(select_info_dict, index=[0])
        return select_info_dict
  
    def get_user_tweets(self, since_id=None, max_id=None, num_tweets=0):
        '''
        Gets last ~3200 tweets from user
        '''
        return pd.DataFrame([status._json for status in tweepy.Cursor(self.api.user_timeline, id=self.id, since_id=since_id, max_id=max_id, tweet_mode='extended').items(num_tweets)])
    
    def get_tweets_from_tweet_id_list(self, id_list=[1308815533052133382]):
        '''
        Gets tweets from user from a tweet id list
        '''
        return pd.DataFrame([self.api.get_status(id=id)._json for id in id_list])
    
def get_tweepy_date_id(time_id_file='time_ids.csv', date='2/1/2020'):
    '''
    Function to return tweet id from given date
    '''
    loaded_time_df=pd.read_csv(time_id_file, index_col=0)
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

def get_date_id(date, time_id_file='time_ids.csv'):
    '''
    Function to get time id from date
    '''
    time_id=get_tweepy_date_id(time_id_file, date)
    if type(time_id) is int:
        return [True, time_id]
    else:
        return [False, 'Try a different date, from 1/1/2020-9/29/2020']
    
def check_date_validity(since_valid=False, until_valid=False):
    '''
    Function to check if date ranges are valid. While either date validity is False, will request
    the user to enter a different date. Valid dates are present in time_ids.csv
    '''
    while since_valid is False or until_valid is False:
        since_date, until_date=get_date_range() #Get dates
        since_valid, since_id=get_date_id(since_date) #Get date validity and date id for date #1
        until_valid, until_id=get_date_id(until_date) #Get date validity and date id for date #2
        print(f'Date #1 valid?: {since_valid}-->{since_date}: {since_id}; Date #2 valid?: {until_valid}-->{until_date}: {until_id}')
    return [since_id, until_id]
                         
def scrape_user_tweets(api, user, since_id, until_id):
    '''
    Function to scrape and return dataframe of tweets for individual users
    '''
    tweets=Tweepy_User(api, user)
    tweet_df=tweets.get_user_tweets(since_id=since_id, max_id=until_id)
    return tweet_df

def scrape_and_save_tweets_from_user_list(api, user_list, output_file, since_id, until_id):
    '''
    Function to scrape and save tweets in csv files given a list of users
    '''
    for user in user_list:
        tweet_df=scrape_user_tweets(api, user, since_id, until_id) #Scrape tweets
        if tweet_df.empty: continue #skips user if tweets not present in specified date range
        select_tweet_info=['created_at','id','full_text','entities','in_reply_to_status_id',
                           'in_reply_to_user_id','in_reply_to_screen_name','user',
                           'is_quote_status', 'retweet_count','favorite_count',
                           'favorited','retweeted','lang']
        select_tweet_df=tweet_df[select_tweet_info]
        if user==user_list[0]:
            #starts new file for first twitter user in list
            select_tweet_df.to_csv(output_file, index=None) 
        else:
            #appends to file for subsequent users in user list
            select_tweet_df.to_csv(output_file, mode='a', header=False, index=None) 
        print(f'{user} saved!')
    pass
    