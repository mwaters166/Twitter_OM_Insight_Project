
'''
Tests for tweepy inputs. Requires pytest.

-Michele Waters
'''
#pip install pytest
from scrape_tweets_tweepy_functions import *
import pdb

loaded_time_df=pd.DataFrame([{'date':'2/1/2020', 'id': 1}, {'date':'2/2/2020', 'id': 2}, {'date':'2/3/2020', 'id': 3}])
    
def test_get_tweepy_date_id():
    '''
    Function to return tweet id from given date
    '''
    date='2/2/2020'
    assert get_tweepy_date_id(loaded_time_df, date) == 2
        
def test_check_date_validity(since_valid=False, until_valid=False, since_date='2/1/2020', until_date='2/3/2020'):
    '''
    Function to check if date ranges are valid. While either date validity is False, will request
    the user to enter a different date. Valid dates are present in time_ids.csv
    '''
    while since_valid is False or until_valid is False:
        since_date, until_date=[since_date, until_date] #Get dates
        since_valid, since_id=get_date_id(since_date, loaded_time_df) #Get date validity and date id for date #1
        until_valid, until_id=get_date_id(until_date, loaded_time_df) #Get date validity and date id for date #2
        print(f'Date #1 valid?: {since_valid}-->{since_date}: {since_id}; Date #2 valid?: {until_valid}-->{until_date}: {until_id}')
    assert [since_id, until_id]==[1, 3]
