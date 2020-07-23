![Twitter_OM](https://github.com/mwaters166/Twitter_OM_Insight_Project/blob/master/twit_pic.png)

# Twitter OM

## Insight Data Science Project by Michele Waters

* Goal: Create a tool for business employees to forecast significantly negative responses on Twitter, using a Twitter "Ratio" (the ratio of the number of comments on a tweet compared to the number of 'likes' on a tweet) as a metric.

### Website:

* Outrage Machine Website: http://winsightanalytics.net:8501/

### Methods:

* Scraped over 200K tweets from ~January 2019-June 2020 from over 100 verified Twitter users across government, entertainment, industy, and news media using Tweepy.

* Collected Twitter account information (i.e. number of followers, number of public lists, status count, etc.) using Twython/ Twitter api.

* Tweets with <50 comments and over ~200K replies or ~900K likes were excluded from the analysis (these outliers tended to represent extremely positive sentiment).

* "Ratioed" tweets (tweets with #comments/#likes >1) only represented ~1% of total dataset. Therefore the majority class (non-ratioed tweets) were randomly undersampled to balance the two classes.

* Tweet text underwent processing and cleaning by replacing contractions, removing stop words & punctuation, and tokenization & lemmatization using spaCy and nltk. 

* Urls and hashtags were encoded; features for whether a hashtag or url was present, word count, & user category were also included as features

* Experimented with TF-IDF, Vader Sentiment Analysis, and GloVe word embedding with Logistic Regression, Random Forest and LSTM in Jupyter Notebook (descriptions of files in 'Files Added' section below)

### Results: 

* The top 25 features included the # of public lists the user was on, #followers, #statuses, the user category, whether there were hashtags & urls present as well as tweet vectors.

* Vader sentiment analysis demonstrated that ratioed tweets tended to be rated more negatively than non-ratioed tweets, while TF-IDF showed that political words tended to be important features of ratioed tweets. Interestingly, US states of conservative senators (who are ratioed frequently on Twitter) also appeared in the list of top TF-IDF word features.

* After removing highly correlated features and looking at feature importance using the consensus of sklearn and eli5 permutation, it was observed that using only follower count with GloVe tweet vectors allowed for the creation of a simplified model, that did not drastically adversely impact its overall performance.

* The final product (http://winsightanalytics.net:8501/) uses GloVe and Logistic Regression to predict ratios from tweet vectors. This is in combination with a follower count Random Forest model, used to predict the error in the probability of being ratioed. 

* The product was implemented using a Streamlit dashboard, with the final model accounting for >80% accuracy, recall, & precision for validation data.

* Overall, the model performance would likely benefit from having a greater diversity of accounts included in the analysis & a larger collection of ratioed tweets in the training data set. Future iterations of this product may include altering the sampling strategy.

### Files Added:

* 1_Scrape_Tweets_Tweepy.py : Python file to scrape tweets from provided usernames and save as individual csv files using Tweepy. Run from terminal: 'python3 1_Scrape_Tweets_Tweepy.py'

* 2_Clean_CSV_to_SQL.py : Python file to merge csv files from individual users and save in SQL database. Run from terminal: 'python3 2_Clean_CSV_to_SQL.py'

* 3_Get_Twitter_User_Data_Twython_no_key.py : Python file to get individual twitter user data (i.e. description, follower counts, etc.) using Twython. Requires Twitter developer keys. Run from terminal: '3_Get_Twitter_User_Data_Twython_no_key.py'

* 4_Clean_Text_Label_Categories_Merge_Tables_Data_Manipulation.ipynb : Jupyter notebook for hand-categorizing user accounts, merging tables, label encoding hashtags/urls, and cleaning (tokenizing, stemming, lemmatizing) twitter text data.

* 5_EDA_Clustering.ipynb : Jupyter notebook for exploratory data analysis (EDA) and KMeans clustering of tweet data in sklearn.

* 6_NLP_TFIDF_GloVe_Vader_Logistic_Regression_v4.ipynb: Jupyter notebook for preliminary NLP analysis of Ratios using TF-IDF, GloVe, Vader Sentiment Analysis, and Logistic Regression

* 7_Twitter_200D_GloVe_LSTM_v2.ipynb: Jupyter notebook for preliminary NLP analysis of Ratios using GloVe LSTM with Keras

* Main Dashboard Files: 1) Dashboard: 'Twitter_Streamlit_Dash.py', 2) Dashboard has dependency on: 'OM_functions.py'

* Model Files: 1) GloVe vectors, only for unique words found in training and validation data set: 'unique_glove_vectors.pkl', 2) Assemble/Scale GloVe Vectors: 'glove_scaler.sav', 3) GloVe/Logistic Regression Model: 'glove_clf.sav', 4) Follower count scaler: 'follower_scaler.sav', 5) Follower Count/Random Forest Residual Modification for Logistic Regression Model: 'follower_rf.sav'

