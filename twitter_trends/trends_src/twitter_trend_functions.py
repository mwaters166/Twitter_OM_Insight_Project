'''
Functions to scrape top 50 twitter trends in US from Trendogate.com, using BeautifulSoup

Michele Waters
'''
import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime as dt
import sys
import time

def progress_bar(percent, bar_length = 20):
    '''Display progress bar.'''
    sys.stdout.write("\r")
    bar = ""
    for i in range(bar_length):
        if i < int(bar_length * percent):
            bar += "*"
        else:
            bar += ""
    sys.stdout.write("Progress: [ %s ] %.2f%%" % (bar, percent * 100))
    sys.stdout.flush()
    pass

def get_twitter_trends(date='2020-06-01', place_id='23424977'):
    '''Get twitter trends given a date. Default date is June 1, 2020; default location id \
    corresponds to United States: 23424977. Returns top 50 trends from Trendogate.com © 2015-2020. \
    Enter date from '2015-02-21' to ~two days prior to current date (last date verified: '2020-10-29').
    '''
    response=requests.get(f'https://trendogate.com/placebydate/{place_id}/{date}')
    parser = BeautifulSoup(response.content, 'html.parser')
    trend_list=[trend.contents[0].replace('#', '').strip().lower() for trend in parser.select("a[href*=trend]")]
    return trend_list

def get_date_interval_list(start_date='2020-06-01', end_date='2020-06-05'):
    '''Get list of dates between start date and end date, converted to '2020-06-21' format '''
    start_dt=dt.datetime.strptime(start_date, '%Y-%m-%d')
    end_dt=dt.datetime.strptime(end_date, '%Y-%m-%d')
    date_list=[dt.datetime.strftime(start_dt+dt.timedelta(days=i),'%Y-%m-%d')  for i in range((end_dt-start_dt).days)]
    return date_list

def save_twitter_trends_date_interval(start_date='2020-06-01', end_date='2020-06-05', place_id='23424977', output_file='./trend_data/twitter_trends.csv'):
    ''' Uses 'get_twitter_trends' function to return dataframe of top 50 trends for given time interval \
    [from start date (inclusive) to end date (exclusive)]. Returned dataframe includes a 'date' column \
    and a 'top_50_trends' column with a list of trends.
    '''
    date_list= get_date_interval_list(start_date, end_date)#get list of dates 
    i=0
    interval_len=len(date_list)
    for date in date_list:
        trend_df=pd.DataFrame({'date': date, 'top_50_trends':[get_twitter_trends(date=date)]}, index=[i])
        if i==0:
            trend_df.to_csv(output_file)
        else:
            trend_df.to_csv(output_file, mode='a', header=False)
            progress_bar((i+1)/interval_len) #display progress bar
        i+=1
    pass 

def run_save_trends(place_id='23424977', output_file='./trend_data/twitter_trends.csv'):
    '''
    Gets start and end date for get_twitter_trends_date_interval function and saves results to file.
    '''
    start_date=input("Enter start date(e.g. 2020-06-01: ")
    end_date=input("Enter end date(e.g. 2020-06-10: ")
    save_twitter_trends_date_interval(start_date, end_date, place_id, output_file)
    return print(f'\nTrends saved to {output_file}!')

    