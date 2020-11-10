![Twitter_OM](https://github.com/mwaters166/Twitter_OM_Insight_Project/blob/master/images/twit_pic.png)

# Twitter OM

## Insight Data Science Project by Michele Waters

* Goal: Create a tool for business employees to forecast significantly negative responses on Twitter, using a Twitter "Ratio" (the ratio of the number of comments on a tweet compared to the number of 'likes' on a tweet) as a metric.

### Website:

* Outrage Machine Website: http://winsightanalytics.net:8501/

### Methods:

* Scraped over 200K tweets from ~January 2019-June 2020 from over 100 verified Twitter users across government, entertainment, industy, and news media using GetOldTweets3 and Tweepy.

* Collected Twitter account information (i.e. number of followers, number of public lists, status count, etc.) using Twython/ Twitter api.

* Tweets with <50 comments and over ~200K replies or ~900K likes were excluded from the analysis (these outliers tended to represent either neutral or extremely positive sentiment).

* "Ratioed" tweets (tweets with #comments/#likes >1) only represented ~1% of total dataset (represented in orange and yellow in the figure below [i.e. 'd_log_ratio'>0]). Therefore the majority class (non-ratioed tweets) were randomly undersampled to balance the two classes.

![Ratio_Distribution](https://github.com/mwaters166/Twitter_OM_Insight_Project/blob/master/images/Ratio%20Distribution.png)

* Tweet text underwent processing and cleaning by replacing contractions, removing stop words & punctuation, and tokenization & lemmatization using spaCy and nltk. 

* Urls and hashtags were encoded; features for whether a hashtag or url was present, word count, & user category were also included as features.

* Experimented with TF-IDF, Vader Sentiment Analysis, and GloVe word embedding with Logistic Regression, Random Forest and LSTM in Jupyter Notebook (descriptions of files in 'Files Added' section below).

### Results: 

* The top 25 features included the # of public lists the user was on, #followers, #statuses, the user category, whether there were hashtags & urls present as well as tweet vectors.

* Vader sentiment analysis demonstrated that ratioed tweets tended to be rated more negatively than non-ratioed tweets, while TF-IDF showed that political words tended to be important features of ratioed tweets. 

* After removing highly correlated features and looking at feature importance using the consensus of sklearn and eli5 permutation, it was observed that using only follower count with GloVe tweet vectors allowed for the creation of a simplified model, that did not drastically adversely impact its overall performance.

* The final product (http://winsightanalytics.net:8501/) uses GloVe and Logistic Regression to predict ratios from tweet vectors. This is in combination with a follower count Random Forest model, used to predict the error in the probability of being ratioed. 

* The product was implemented using a Streamlit dashboard, with the final model accounting for >80% accuracy, recall, & precision for validation data.

* Overall, the model performance would likely benefit from having a greater diversity of accounts included in the analysis & a larger collection of ratioed tweets in the training data set. Future iterations of this product may include altering the sampling strategy.

### Files Added:

* 'final model' folder-- Contains all files needed to run final model (deployed using Streamlit dashboard, run on AWS EC2 using ubuntu). This folder includes the following:

  * Main Dashboard Files: 1) Dashboard: 'Twitter_Streamlit_Dash.py', 2) Dashboard has dependency on: 'OM_functions.py' (all functions related to text processing, vectorization, & running the model), which has dependency on 'Tweet_Class_NLP.py' (tweet class to perfom NLP functions using spaCy and nltk). To run the dashboard locally,(from the final_model folder) run from terminal: 'streamlit run Twitter_Streamlit_Dash.py'. To install 'requirements.txt', run from terminal: 'pip install -r requirements.txt'

  * Model Files: 1) GloVe vectors, only for unique words found in training and validation data set: 'unique_glove_vectors.pkl', 2) Assemble/Scale GloVe Vectors: 'glove_scaler.sav', 3) GloVe/Logistic Regression Model: 'glove_clf.sav', 4) Follower count scaler: 'follower_scaler.sav', 5) Follower Count/Random Forest Residual Modification for Logistic Regression Model: 'follower_rf.sav'
  
* 'src' folder-- Contains files related to scraping tweets. Note: Originally, GetOldTweets3 was used to obtain tweets for the majority of this project, however support for this tool appears to have ended. Updated tweet scraper files include:
  * '1_Scrape_Tweets_Tweepy.py' and 'scrape_tweets_tweepy_functions.py'. These files scrape tweets with Tweepy (which requires Twitter Developer credentials) and can be used by running './run.sh' from command line in main directory. Currently, the run.sh file takes 'users_test.csv' as the input file (which contains two twitter handle examples to scrape) and outputs all tweets to 'tweets.csv'. You can modify 'users_test.csv' with different users or change the run.sh file to collect twitter handles from 'users.csv' to scrape full dataset used in this project.
  * 'example_env.txt' -- example .env file. Before using the running the './run.sh' file you MUST add your Twitter api keys to this file and rename it '.env'. (This replaces previous version, that asked the user to input their api keys.)
  
* 'users' folder-- Contains example csv files with twitter handles for Tweepy scraper

* 'time_id_data' folder-- Contains files required to create 'time_ids.csv', which is a csv file containing tweet ids that correspond to specific dates, to better control time intervals in Tweepy
  
* 'tweet_data' folder-- Folder for tweet/Tweepy output to 'tweets.csv'. Contains example output from users_test.csv

* 'images' folder-- Contains images displayed in repository

* 'notebooks_cleaning_eda_model_testing' folder-- Jupyter Notebooks and python files for data cleaning, data exploration, and model testing. This folder includes the following:

  * 1_Scrape_Tweets_Tweepy_Time_Ids.ipynb: Jupyter notebook outlines process of developing a tweet_id dictionary that corresponds to times and scraping tweets from specific users using Tweepy

  * 2_Clean_CSV_to_SQL.py : Python file to merge csv files from individual users and save in SQL database. Run from terminal: 'python3 2_Clean_CSV_to_SQL.py'

  * 3_Get_Twitter_User_Data_Twython_no_key.py : Python file to get individual twitter user data (i.e. description, follower counts, etc.) using Twython. Requires Twitter developer keys. Run from terminal: '3_Get_Twitter_User_Data_Twython_no_key.py'

  * 4_Clean_Text_Label_Categories_Merge_Tables_Data_Manipulation.ipynb : Jupyter notebook for hand-categorizing user accounts, merging tables, label encoding hashtags/urls, and cleaning (tokenizing, stemming, lemmatizing) twitter text data.

  * 5_EDA_Clustering.ipynb : Jupyter notebook for exploratory data analysis (EDA) and KMeans clustering of tweet data in sklearn.
  
  * 6-5_NLP_GloVe_Vader_Logistic_Regression_Oversample_v5.ipynb: Jupyter notebook for preliminary NLP analysis of Ratios, experimenting with oversampling and GloVe-Vader Sentiment Analysis-Logistic Regression model

  * 7_Twitter_200D_GloVe_LSTM_v2.ipynb: Jupyter notebook for preliminary NLP analysis of Ratios using GloVe LSTM with Keras
  
  * 8_Twitter_OM_PySpark_SQL.ipynb: Jupyter notebook for preliminary experimentation in PySpark/SQL and examination of users associated with ratioed tweets
  
* 'twitter_trends' folder-- Contains files related to scraping top 50 trending topics in US from trendogate.com using BeautifulSoup. This folder contains 'trends_src/scrape_twitter_trends.py', which has dependency on 'trends_src/twitter_trend_functions.py'. From 'twitter_trends' folder, run from terminal: './run_trends.sh' and enter date interval in format prompted to have top 50 trends saved to 'trend_data/test_twitter_trends.csv' (default from run_trends.sh file). Trend data for 1/01/2019-10/29/2020 can be found in twitter_trends/trend_data/'twitter_trends.csv'.

### The Twitter Ratio in Popular Culture:

* "The Ratio Establishes Itself on Twitter"-- New York Times: https://www.nytimes.com/interactive/2018/02/09/technology/the-ratio-trends-on-twitter.html

* "How to Know if You've Sent a Horrible Tweet"-- Esquire: https://www.esquire.com/news-politics/news/a54440/twitter-ratio-reply/

* Merriam-Webster: https://www.merriam-webster.com/words-at-play/words-were-watching-ratio-ratioed-ratioing


