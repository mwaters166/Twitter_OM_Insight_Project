import pandas as pd
import tweepy

class Tweet_Builder():
    '''
    Creation of Tweet_Builder, initialized by api and instance of Twitter_User class
    '''
    def __init__(self, api, twitter_user):
        self.api=api
        self.user=self.api.get_user(twitter_user)
        self.id=self.user.id
  
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