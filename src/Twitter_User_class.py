import pandas as pd
import tweepy

class Twitter_User():
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
    
