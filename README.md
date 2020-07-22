![Twitter_OM](https://github.com/mwaters166/Twitter_OM_Insight_Project/blob/master/twit_pic.png)

# Twitter OM

## Insight Data Science Project by Michele Waters

* Goal: Create a tool for business employees to forecast significantly negative responses on Twitter 

### Website:

* Outrage Machine Website: http://winsightanalytics.net:8501/

### Files added:

* 1_Scrape_Tweets_Tweepy.py : Python file to scrape tweets from provided usernames and save as individual csv files using Tweepy. Run from terminal: 'python3 1_Scrape_Tweets_Tweepy.py'

* 2_Clean_CSV_to_SQL.py : Python file to merge csv files from individual users and save in SQL database. Run from terminal: 'python3 2_Clean_CSV_to_SQL.py'

* 3_Get_Twitter_User_Data_Twython_no_key.py : Python file to get individual twitter user data (i.e. description, follower counts, etc.) using Twython. Requires Twitter developer keys. Run from terminal: '3_Get_Twitter_User_Data_Twython_no_key.py'

* 4_Clean_Text_Label_Categories_Merge_Tables_Data_Manipulation.ipynb : Jupyter notebook for hand-categorizing user accounts, merging tables, label encoding hashtags/urls, and cleaning (tokenizing, stemming, lemmatizing) twitter text data.

* 5_EDA_Clustering.ipynb : Jupyter notebook for exploratory data analysis (EDA) and KMeans clustering of tweet data in sklearn.

* 6_NLP_TFIDF_GloVe_Vader_Logistic_Regression_v4.ipynb: Jupyter notebook for preliminary NLP analysis of Ratios using TF-IDF, GloVe, Vader Sentiment Analysis, and Logistic Regression

* 7_Twitter_200D_GloVe_LSTM_v2.ipynb: Jupyter notebook for preliminary NLP analysis of Ratios using GloVe LSTM with Keras

* Main Dashboard Files: 1) Dashboard: 'Twitter_Streamlit_Dash.py', 2) Dashboard has dependency on: 'OM_functions.py'

* Model Files: 1) GloVe vectors, only for unique words found in training and validation data set: 'unique_glove_vectors.pkl', 2) Assemble/Scale GloVe Vectors: 'glove_scaler.sav', 3) GloVe/Logistic Regression Model: 'glove_clf.sav', 4) Follower count scaler: 'follower_scaler.sav', 5) Follower Count/Random Forest Residual Modification for Logistic Regression Model: 'follower_rf.sav'

