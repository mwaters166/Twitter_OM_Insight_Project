'''
Functions to scrape tweets using Tweepy
using tweet ids corresponding to 
specific dates

-Michele Waters
'''


import pandas as pd
import tweepy

#Get twitter handles/user names of accounts to scrape
def get_users(file_name='users.csv'):
    users=list(pd.read_csv(file_name).users)
    return users

#Get twitter developer keys and tokens
def get_api_tokens():
    api_key=input('Enter api_key: ')
    api_secret_key=input('api_secret_key: ')
    access_token=input('access_token: ')
    access_token_secret=input('access_token_secret: ')
    return [api_key, api_secret_key, access_token, access_token_secret]

#Function to authorize api with keys and tokens
def auth_api(api_key, api_secret_key, access_token, access_token_secret):
    auth = tweepy.OAuthHandler(api_key, api_secret_key)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, wait_on_rate_limit=True) 
    return api

#Creation of Tweepy class
class Tweepy():
    def __init__(self, api, user_name):
        self.api=api
        self.user=api.get_user(user_name)
        self.id=self.user.id
        self.follower_num=self.user.followers_count
        self.friend_num=self.user.friends_count
        
    #Gets user account information, returning select attributes
    def get_user_info_df(self, result='dictionary'):
        select_attributes=['screen_name','name','id', 'profile_location', 'description',\
                           'protected','followers_count', 'friends_count', 'listed_count', \
                           'created_at','profile_image_url','favourites_count','verified', \
                           'statuses_count','lang']
        select_info_dict={k:v for k, v in self.user._json.items() if k in select_attributes}
        if result=='df':
            select_info_dict=pd.DataFrame(select_info_dict, index=[0])
        return select_info_dict
    
    #Gets last ~3200 tweets from user
    def get_user_tweets(self, since_id=None, max_id=None, num_tweets=0):
        return pd.DataFrame([status._json for status in tweepy.Cursor(self.api.user_timeline, id=self.id, since_id=since_id, max_id=max_id, tweet_mode='extended').items(num_tweets)])
    
    #Gets tweets from user from a tweet id list
    def get_tweets_from_tweet_id_list(self, id_list=[1308815533052133382]):
        return pd.DataFrame([self.api.get_status(id=id)._json for id in id_list])
    
#Function to return tweet id from given date
def get_tweepy_date_id(time_id_file='time_ids.csv', date='2/1/2020'):
    loaded_time_df=pd.read_csv(time_id_file, index_col=0)
    time_dict={record['date']:record['id'] for record in loaded_time_df.to_dict('records')}
    if date in time_dict:
        return time_dict[date]
    else:
        return 'Date not present; choose a different date'
    
#Function to check if date ranges are valid
#Example entries: since_date: 6/1/2020 , until_date: 9/29/2020
def get_date_ranges(time_id_file='time_ids.csv'):
    not_valid=True
    while not_valid:
        since_date=input("Enter start date for scraping (e.g. 9/1/2020): ")
        since_id= get_tweepy_date_id(time_id_file='time_ids.csv', date=since_date)                
        until_date=input("Enter end date for scraping (e.g. 9/29/2020): ")
        until_id= get_tweepy_date_id(time_id_file='time_ids.csv', date=until_date)
        if type(since_id) is int and type(until_id) is int:
            not_valid=False
        else:
            print('One or more dates are not valid. Try again.')
    return [since_id, until_id]
                         
#Function to scrape and return dataframe of tweets for individual users
def scrape_user_tweets(api, user, since_id, until_id):
    tweets=Tweepy(api, user)
    tweet_df=tweets.get_user_tweets(since_id=since_id, max_id=until_id)
    return tweet_df

#Function to scrape and save tweets in csv files given a list of users
def scrape_and_save_tweets_from_user_list(api, user_list, output_file, since_id, until_id):
    for user in user_list:
        tweet_df=scrape_user_tweets(api, user, since_id, until_id) #Scrape tweets
        if tweet_df.empty: continue
        select_tweet_info=['created_at','id','full_text','entities','in_reply_to_status_id',
                           'in_reply_to_user_id','in_reply_to_screen_name','user',
                           'is_quote_status', 'retweet_count','favorite_count',
                           'favorited','retweeted','lang']
        select_tweet_df=tweet_df[select_tweet_info]
        if user==user_list[0]:
            select_tweet_df.to_csv(output_file, index=None)
        else:
            select_tweet_df.to_csv(output_file, mode='a', header=False, index=None)
        print(f'{user} saved!')
    pass
    