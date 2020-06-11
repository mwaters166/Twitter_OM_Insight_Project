#!/usr/bin/env python
# coding: utf-8

# Scrape Tweets from  users and save to csv files in main directory

from collections import defaultdict
import os, sys
import time
import GetOldTweets3 as got
import numpy as np
import pandas as pd

os.makedirs('tweet_data', exist_ok=True)
df_list=[]

users = [
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
         "realdonaldtrump",
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

end_date="2019-01-01"
for username in list(users):
    print(username)
    count = -1
    # Creation of query object                                                                                                                                                                                      
    tweetCriteria = got.manager.TweetCriteria().setUsername(username)\
                                               .setMaxTweets(count)\
                                               .setSince(end_date) 
    # Creation of list that contains all tweets                                                                                                                                                                     
    tweets = None
    for ntries in range(5):
        try:
            tweets = got.manager.TweetManager.getTweets(tweetCriteria)
        except SystemExit:
            print("Trying again in 15 minutes.")
            time.sleep(15*60)
        else:
            break
    if tweets is None:
        print("Failed after 5 tries, quitting!")
        exit(1)

    data = defaultdict(list)
    for t in tweets:
        data["username"].append(username)
        data["tweet_id"].append(t.id)
        data["text"].append(t.text)
        data["url_attached"].append(t.urls)
        data["hashtags"].append(list(set(t.hashtags.split())))
        data["retweets"].append(t.retweets)
        data["favorites"].append(t.favorites)        
        data["reply_count"].append(t.replies)
        data["reply_to"].append(t.to)
        data["date"].append(t.date)
        data["formatted_date"].append(t.formatted_date)
        data["geo"].append(t.geo if t.geo != "" else None)
        data["to"].append(t.to)
        data["author_id"].append(t.author_id)
        data["link_to_tweet"].append(t.permalink)
       
    df = pd.DataFrame(data, columns=["username","tweet_id","text","url_attached","hashtags","retweets","favorites","reply_count","reply_to","date","formatted_date","geo","to","author_id","link_to_tweet"])
    df['ratio_comment_like']=df.reply_count/df.favorites 
    df['ratio_comment_retweet']=df.reply_count/df.retweets
    df['log_ratio']=np.log(df.reply_count/df.favorites)
    #Ratio Richter scale: 𝐿𝑛( 𝑇𝑤𝑖𝑡𝑡𝑒𝑟 𝑅𝑎𝑡𝑖𝑜)∗𝐿𝑜𝑔(𝑅𝑒𝑝𝑙𝑖𝑒𝑠)
    df['ratio_richter_likes']=np.log(df.reply_count/df.favorites)*np.log10(df.reply_count)
    df['ratio_richter_retweets']=np.log(df.reply_count/df.retweets)*np.log10(df.reply_count)
    df.to_csv(f'{username}_{end_date}_present.csv')
    df_list.append(df)
    #To compress files
    #df.to_pickle(f"tweet_data/{username}.pkl.gz", compression="gzip")
print("Done!")




