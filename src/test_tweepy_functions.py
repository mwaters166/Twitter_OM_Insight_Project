
'''
Tests for tweepy inputs. Requires pytest.

-Michele Waters
'''
#pip install pytest
from scrape_tweets_tweepy_functions import *

def test_get_users(file_name='../users/users_test.csv'):
    '''
    Get twitter handles/user names of accounts to scrape
    '''
    users=list(pd.read_csv(file_name).users)
    assert users==['serenawilliams', 'barackobama']
    
def test_get_tweepy_date_id(time_id_file='../time_ids.csv', date='2/1/2020'):
    '''
    Function to return tweet id from given date
    '''
    loaded_time_df=pd.read_csv(time_id_file, index_col=0)
    time_dict={record['date']:record['id'] for record in loaded_time_df.to_dict('records')}
    if date in time_dict:
        assert time_dict[date] == 1223395561912573952
        
def test_check_date_validity(since_valid=False, until_valid=False):
    '''
    Function to check if date ranges are valid. While either date validity is False, will request
    the user to enter a different date. Valid dates are present in time_ids.csv
    '''
    while since_valid is False or until_valid is False:
        since_date, until_date=['1/1/2020', '9/29/2020'] #Get dates
        since_valid, since_id=get_date_id(since_date, '../time_ids.csv') #Get date validity and date id for date #1
        until_valid, until_id=get_date_id(until_date, '../time_ids.csv') #Get date validity and date id for date #2
        print(f'Date #1 valid?: {since_valid}-->{since_date}: {since_id}; Date #2 valid?: {until_valid}-->{until_date}: {until_id}')
    assert [since_id, until_id]==[1212161809018437633, 1310731279176998913]       