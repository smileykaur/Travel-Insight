"""
Step 2 : Data aggregation: aggregate data to generate text corpus:
This will clean the raw data that was gathered from Reddit -
- convert data to format that can be directly consumed by Dataframes,
"""
import pandas as pd
import os
from .config import (
    AGG_BY_SUB,
    COMMENTS_COLS,
    REPLIES_COLS,
)


class DataPreprocessing:
    def __init__(self):
        self.RAW_SUBMISSIONS = "../data/submission.tsv"
        self.RAW_COMMENTS = "../data/comments.tsv"
        self.RAW_REPLIES = "../data/replies.tsv"

    def generate_clean_source_files(self):
        # load data after handling exceptions
        self.df_submissions = pd.read_csv(self.RAW_SUBMISSIONS, sep='\t')
        self.df_comments = pd.DataFrame(self.generate_dataframe(self.RAW_COMMENTS, COMMENTS_COLS))
        self.df_replies = pd.DataFrame(self.generate_dataframe(self.RAW_REPLIES, REPLIES_COLS))

        # TODO: Load this data to Database (serve as main data source)
        # write df to csv
        #self.load_df_to_csv()

    def load_df_to_csv(self):
        # writing df to csv-
        source_data_dir = "../data/" + "source_data/"
        if not os.path.exists(source_data_dir):
            os.mkdir(source_data_dir)

        self.df_submissions.to_csv("{0}submission.csv".format(source_data_dir))
        self.df_comments.to_csv("{0}comments.csv".format(source_data_dir))
        self.df_replies.to_csv("{0}replies.csv".format(source_data_dir))

    def generate_dataframe(self, input_file, columns_list):
        """
        Generate a dataframe for given set of inputs
        :param columns_list: List of column names
        :return:
            Dictionary for Dataframe
        """
        data_dict = dict([(key, []) for key in columns_list])
        # read file
        with open(input_file, "r") as filereader:
            filereader.readline()
            for line in filereader:
                try:
                    data = line.strip().split("\t")
                    if len(data) == len(columns_list):
                        for _col_ind, _col_name in enumerate(columns_list):
                            data_dict[_col_name].append(data[_col_ind])
                except Exception as ex:
                    # logging.warning("trouble reading the record due to {}".format(ex))
                    # TODO: Set up a logger
                    print("trouble reading the record due to {}".format(ex))
        return data_dict

    def aggregate_replies_to_comments(self,):
        """
        1. Roll up Replies at comment level for each 'submission_id', 'comment_id'
        ['submission_id', 'submission_topic', 'comment_id', 'text]
        Group replies and roll up to comments_id

        Output: Generate .csv file

        :return: None
        """
        # group replies by comment_id
        grouped_replies = self.df_replies.groupby(['comments_id'])['reply']\
            .apply(lambda x: "%s" % ','.join(x)).reset_index()
        # merging grouped replies with comments
        grouped_comments = pd.merge(self.df_comments[['comments_id', 'comment_date', 'submission_id', 'comment']],
                                    grouped_replies, on='comments_id')
        grouped_comments['comment'] = grouped_comments['comment'] + grouped_comments['reply']

        # Output aggregated comments
        output_loc = "../data/aggregated_data/"
        if not os.path.exists(output_loc):
            os.mkdir(output_loc)

        df_grouped_comments = grouped_comments[['comments_id', 'comment_date', 'submission_id', 'comment']]
        df_grouped_comments.to_csv(output_loc+"group_by_comments.csv", index=False)

        # Aggregate aggregated comments by submission_id
        self.aggregate_comments_to_submission(df_grouped_comments, output_loc)
        return

    def aggregate_comments_to_submission(self, df_grouped_comments, output_loc):
        """
        Roll up replies and comments for each 'submission_id' that generate all text for a submission
        ['submission_id', 'submission_topic', 'text']

        Output: Generate .csv file

        :return: None
        """
        # group comments by submission_id
        grouped_comments = df_grouped_comments.groupby(['submission_id'])['comment']\
            .apply(lambda x: "%s" % ','.join(x)).reset_index()
        # merging grouped comments with submission
        grouped_submissions = pd.merge(self.df_submissions[['submission_id', 'submission_date', 'title']],
                                       grouped_comments, on='submission_id')

        df_grouped_submissions = grouped_submissions[['submission_id', 'submission_date', 'title', 'comment']]
        df_grouped_submissions.to_csv(output_loc + "group_by_submissions.csv", index=False)
        return


    def aggregate_by_month(self):
        """
        aggregate by month and year for each of DF and then aggregate

        :return:
        """
        # TODO: aggregate by month
        # aggregate replies by month , year
        # aggregate comments by month , year
        # generate the counter - This will be substituted by SQL
        #
        return
