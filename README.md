# Twitter_OM_Insight_Project

## Insight Data Science Project by Michele Waters

* Goal: Create a tool for business employees to forecast significantly negative responses on Twitter 

### Files added:

* 1_Scrape_Tweets_Tweepy.py : Python file to scrape tweets from provided usernames and save as individual csv files using Tweepy. Run from terminal: 'python3 1_Scrape_Tweets_Tweepy.py'

* 2_Clean_CSV_to_SQL.py : Python file to merge csv files from individual users and save in SQL database. Run from terminal: 'python3 2_Clean_CSV_to_SQL.py'

* 3_Get_Twitter_User_Data_Twython_no_key.py : Python file to get individual twitter user data (i.e. description, follower counts, etc.) using Twython. Requires Twitter developer keys. Run from terminal: '3_Get_Twitter_User_Data_Twython_no_key.py'

* 4_Clean_Text_Label_Categories_Merge_Tables_Data_Manipulation.ipynb : Jupyter notebook for hand-categorizing user accounts, merging tables, label encoding hashtags/urls, and cleaning (tokenizing, stemming, lemmatizing) twitter text data.



