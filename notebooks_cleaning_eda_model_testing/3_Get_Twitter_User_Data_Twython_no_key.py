#!/usr/bin/env python
# coding: utf-8

'''
Code to save twitter user data (including account descriptions and follower counts) to csv and sql 
'''

from twython import Twython
import pandas as pd
import sys
import string
import simplejson

import sqlite3
conn=sqlite3.connect('twitter_data_2019_2020.db')

import datetime
now = datetime.datetime.now()
day=int(now.day)
month=int(now.month)
year=int(now.year)

APP_KEY = 'APP KEY' #Replace with Twitter Developer account App Key
APP_SECRET = 'APP SECRET'#Replace with Twitter Developer account App Secret Key

twitter = Twython(APP_KEY, APP_SECRET, oauth_version=2)

ACCESS_TOKEN = twitter.obtain_access_token()

twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)

twitter.get_application_rate_limit_status()['resources']['search']

#Can only request 100 users at a time with Twitter api, so breaking users up into 2 lists:
users1 = [
         "barackobama",
         "michelleobama",
         "hillaryclinton",
         "speakerpelosi",
         "kamalaharris",
         "ambassadorrice",
         "repadamschiff",
         "joebiden",
         "berniesanders",
         "nycmayor",
         "who",
         "comey",
         "rodrosenstein",
         "cillizzacnn",
         "ac360",
         "donlemon",
         "brianstelter",
         "vanjones68",
         "foxnews",
         "breitbartnews",
         "nra",
         "maggieNYT",
         "bariweiss",
         "washingtonpost",
         "maddow",
         "joenbc",
         "morningmika",
         "billoreilly",
         "seanhannity",
         "tuckercarlson",
         "ingrahamangle",
         "billmaher",
         "joerogan",
         "justinamash",
         "sarahpalinusa",
         "govchristie",
         "rudygiuliani",
         "piersmorgan",
         "mittromney",
         "senatorcollins",
         "lisamurkowski",
         "senatorloeffler",
         "nikkihaley",
         "jerryfalwelljr",
         "scottwalker",
         "tedcruz",
         "repmattgaetz",
         "randpaul",
         "realdonaldtrump",]
users2=[
         "mcuban",
         "kanyewest",
         "kimkardashian",
         "kyliejenner",
         "chrissyteigen",
         "justinbieber",
         "taylorswift13",
         "arianagrande",
         "selenagomez",
         "katyperry",
         "mileycyrus",
         "ddlovato",
         "shakira",
         "britneyspears",
         "jtimberlake",
         "beyonce",
         "rihanna",
         "tigerwoods",
         "snoopdogg",
         "50cent",
         "cthagod",
         "kevinhart4real",
         "chrisbrown",
         "oprah",
         "droz",
         "drdrew",
         "drphil",
         "paula_deen",
         "therealroseanne",
         "loganpaul",
         "jakepaul",
         "shanedawson",
         "oliviajadee",
         "vanessahudgens",
         "leamichele",
         "tip",
         "lancearmstrong",
         "nike",
         "nfl",
         "nba",
         "wellsfargo",
         "equifax",
         "equinox",
         "papajohns",
         "gary_kelly",
         "jeffbezos",
         "billgates",
         "tim_cook",
         "satyanadella",
         "alexisohanian",
         "bchesky",
         "realmikelindell",
         "elonmusk",
         "crossfitceo",
         "drewbrees",
         "kaepernick7",
         "cristiano",
         "fedex",
         "twitter",
         "facebook",
         "reddit",
         "youtube",
         "natesilver538",
        ]

#Get user info for list 1
users_info1 = twitter.lookup_user(screen_name = users1)
#Get user info for list 2
users_info2 = twitter.lookup_user(screen_name = users2)
#Convert list 1 to dataframe
users1_df=pd.DataFrame(users_info1)
#Convert list 2 to dataframe
users2_df=pd.DataFrame(users_info2)

##Field information:
## followers_count: The number of followers this account currently has. Under certain conditions of duress, this field will temporarily indicate “0”. Example:
## friends_count: The number of users this account is following (AKA their “followings”). Under certain conditions of duress, this field will temporarily indicate “0”. Example:
## listed_count: The number of public lists that this user is a member of. Example:
## favourites_count: The number of Tweets this user has liked in the account’s lifetime. British spelling used in the field name for historical reasons.
## statuses_count: The number of Tweets (including retweets) issued by the user. Example:

#Merge two tables in pandas
users_df=pd.concat([users1_df, users2_df])
#Rename id field
users_df=users_df.rename(columns={'id':'account_id'})
#Limit fields to selected below
selected_fields=['account_id','location','screen_name','name','description','url', 'created_at', 'verified','followers_count','friends_count','listed_count', 'favourites_count', 'statuses_count']
#lower screen_name
users_df.screen_name=users_df.screen_name.apply(lambda x: x.lower())
#Create file name with today's date
file_name = "twitter_user_account_info_%i_%i_%i" % (now.month, now.day, now.year)
#Save user info to csv file
users_df[selected_fields].to_csv(f'{file_name}.csv')
#Save user info to sql database
users_df[selected_fields].to_sql(f'{file_name}', conn, index_label='id', if_exists='replace')





