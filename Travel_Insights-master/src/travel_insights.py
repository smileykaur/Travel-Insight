"""
    Author: Amanpreet Kaur (apkruku.17@gmail.com/akaur4@sdsu.edu)

    -------------------------------------------------------------
    TRAVEL INSIGHTS
    -------------------------------------------------------------

    Project is split into following stages -

    Step 1: Data wrangling: get data from Reddit using PRAW
    Step 2: Data aggregation: aggregate data to generate text corpus:
        a. Agg-by-sub: Aggregate `Comments` and `Replies` for each Reddit submission. <give schema>
        b. Agg-by-month: Aggregate `Comments` and `Replies` by each month of a year.
    Step 3: Data Pre-processing: Clean and pre-process data by aggregate (Done in each processing)
    Step 4: Data Analysis: Analyse Agg-by-month data for trends
    Step 5: NLP: Identify entities using Named Entity Recognition
    Step 6: NLP: Topic/Aspect identification
            a. Custom Parser
            b. LDA/TFIDF
            b. Tokenization
    Step 7: Generate word-cloud from the approach for Amazon review summarizer
    """

import sys
import logging
import time
import os
#import re
import pandas as pd
from .data_wrangler import RedditWrangler
from .data_preprocessing import DataPreprocessing
from .trend_analysis import TrendAnalysis
from .named_entity_recognition import NER

TS = time.strftime("%Y-%m-%d:%H-%M-%S")
log_dir = "./logs/"
if not os.path.exists(log_dir):
    os.mkdir(log_dir)
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                    datefmt='%m-%d %H:%M',
                    filename=log_dir+"travel_insights"+str(TS)+".log",
                    filemode='w')

# Step 1:
def get_reddit_data():
    """ Extract data from Reddit using PRAW Library
    :return: None
    """
    # list of subreddits
    subreddits = ["travel"]
    rw = RedditWrangler()
    logging.info("fetch sub-reddit data")
    for _subreddit in subreddits:
        rw.extract_data(_subreddit, top_limit="year", replace_more_limit=10)
    return


# Step 2 & 3:
def aggregate_data():
    agg = DataPreprocessing()
    agg.generate_clean_source_files()
    agg.aggregate_replies_to_comments()


# Step 4:
def activity_trend():
    trend = TrendAnalysis()
    trend.analyze_trend_in_user_activity()


# Step 5:
def get_NER():
    """
    :return:
    """
    data = pd.read_csv("../data/aggregated_data/group_by_submissions.csv")
    obj = NER(data)
    logging.info("generating the NER for each submission")
    obj.NER()


if __name__ == '__main__':
    """
    :return:
    """
    try:
        # Step 1: Collect data from Reddit using Praw Library
        logging.info("getting data from Reddit")
        get_reddit_data()

        # Step 2 & 3: Data aggregation: aggregate by submission_id, comment_id, month+year
        aggregate_data()

        # Step 4: Trend Analysis: Analyze activity trends
        activity_trend()

        # Step 5: Named Entity Recognition:
        get_NER()

    except Exception as ex:
        logging.info("error occured while analyzing {}".format(ex))
