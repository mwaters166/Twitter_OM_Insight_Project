'''
Scrapes top 50 twitter trends in US for user given start date (inclusive)-->end date(exclusive) and saves output to csv file. 

Note: Returns top 50 trends from Trendogate.com © 2015-2020. 

Enter date from '2015-02-21' to approximately two days prior to current date (last date verified: '2020-10-29').

Michele Waters
'''
from twitter_trend_functions import run_save_trends
import sys

output_file=sys.argv[1] #gets output file: './trend_data/twitter_trends.csv'

#place_id '23424977 corresponds to United States; saves results from top 50 trends to output_file  
run_save_trends(place_id='23424977', output_file=output_file)