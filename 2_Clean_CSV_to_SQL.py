#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import sqlite3
from sklearn.impute import SimpleImputer
from sklearn_pandas import DataFrameMapper

conn=sqlite3.connect('twitter_data_2019_2020.db')
cursor= conn.cursor()
users = list(pd.read_csv(file_name).users)

def assemble_df_list(users):
    end_date="2019-01-01"
    df_list=[]
    for user in users:
        df=pd.read_csv(f'{user}_{end_date}_present.csv', index_col=0)
        #Remove values where favorite, retweets, or reply count is zero
        df=df[~((df['favorites']==0) | (df['retweets']==0) | (df['reply_count']==0))]
        df['got_ratioed']=df['ratio_comment_like']>=1.5 #True/False values if ratioed (set threshold at 1.5/2)
        df['got_richter_ratioed']=df['ratio_richter_likes']>=1.5 #True/False values if richter ratioed
        df['d_richter_like_ratio']=round(df['ratio_richter_likes']) #discrete values of richter ratio_likes
        df['d_richter_retweet_ratio']=round(df['ratio_richter_retweets']) #discrete values of richter ratio_rt 
        df=df.drop(columns='geo') #Drop location column; often has missing values
        #Append dataframes to a list
        df_list.append(df)     
    return df_list

df_list= assemble_df_list(users)

#Replace missing values in string/object columns
def replace_missing_df(df):
    #Create steps to replace missing values for each column
    steps=[([col], [SimpleImputer(strategy='constant', fill_value='None')]) for col in df.columns if df[col].dtype=='O']
    #apply mapper to output dataframe and keep all columns
    mapper=DataFrameMapper(steps, df_out=True, default=None)
    #transform/clean dataframe
    clean_df=mapper.fit_transform(df)
    return clean_df

def save_cleaned_dfs(df_list):
    clean_df_list=[]
    end_date="2019-01-01"
    i=0
    for df in df_list:
        clean_df= replace_missing_df(df)
        clean_df_list.append(clean_df)
        #Send cleaned dataframe to SQL database
        clean_df.to_sql(f'{users[i]}_{end_date[:4]}_present', conn, index_label='id', if_exists='replace')
        i+=1
    merged_df= pd.concat(clean_df_list)
    merged_df.to_sql(f'merged_twitter_{end_date[:4]}_present', conn, index_label='id', if_exists='replace')
    return "Done!"

save_cleaned_dfs(df_list)
