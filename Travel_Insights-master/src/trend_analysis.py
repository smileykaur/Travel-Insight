"""
Stage 3:
Analyze activity trends - Submissions, Comments, Replies
"""
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import os

SOURCE_DATA="../data/source_data/"


class TrendAnalysis:
    def __init__(self):
        # analyze for submissions: Submissions are direct intent for travel
        self.df_submission = pd.read_csv(SOURCE_DATA+"submission.csv")
        # analyze for comments:
        self.df_comments = pd.read_csv(SOURCE_DATA+"comments.csv")
        # analyze for replies:
        self.df_replies = pd.read_csv(SOURCE_DATA+"replies.csv")

        # store resulting visualizations
        self.viz_loc = "../viz/trend_analysis/"
        if not os.path.exists(self.viz_loc):
            os.mkdir(self.viz_loc)

    def gen_line_chart(self, data, y_label, title, img_name):
        """
        generate a line_chart
        :param data:
        :param y_label:
        :param title:
        :param img_name:
        :return:
        """
        fig, ax = plt.subplots()
        sns.set(style="whitegrid")
        ax.plot(data.count())
        ax.set_ylabel(y_label)
        ax.set_xlabel('Months')
        ax.set_title(title)
        plt.savefig(self.viz_loc+"{img_name}.png".format(img_name=img_name))

    def gen_distribution_plot(self, data, y_label, title, img_name, x_label="Months"):
        """
        Generate a distribution plot for the records
        :param data:
        :param y_label:
        :param title:
        :param img_name:
        :param x_label:
        :return:
        """
        fig, ax = plt.subplots()
        sns.set(style="whitegrid")
        sns.distplot(data)
        plt.ylabel(y_label)
        plt.xlabel(x_label)
        plt.title(title)
        plt.savefig(self.viz_loc + "{img_name}.png".format(img_name=img_name))

    def gen_histograms(self, data, y_label, title, column_parm, img_name):
        """
        generate histogram for distribution across months
        :param data:
        :param y_label: label for y-axis
        :param title: title for the graph
        :return: None
        """
        fig, ax = plt.subplots()
        sns.set(style="whitegrid")
        ax.set_ylabel(y_label)
        ax.set_xlabel('Months')
        ax.set_title(title)
        plt.hist(data[column_parm])
        fig.tight_layout()
        # plt.show()
        plt.savefig(self.viz_loc+"{img_name}.png".format(img_name=img_name))

    def analyze_trend_in_user_activity(self):
        """
        Analyze the reddit users activity level for a subreddit in a given month.
        Increased user activity in a month indicate user's looking to travel or completing a travel
        :return:
        """
        # Submissions
        self.gen_histograms(self.df_submission, y_label='Submission Counts',
                            title='Trend Analysis for Submission', column_parm='submission_month',
                            img_name='submission_bar_chart')

        self.gen_distribution_plot(self.df_submission.submission_month, y_label='Submission Counts',
                                   title='Trend Analysis for Submission', img_name='submission_dist_chart')

        # Comments
        self.gen_histograms(self.df_comments, y_label='Comments Counts',
                            title='Trend Analysis for Comments',column_parm='comment_month',
                            img_name='comment_bar_chart')

        self.gen_distribution_plot(self.df_comments.comment_month, y_label='comments Counts',
                                   title='Trend Analysis for comments', img_name='comment_dist_chart')

        # Reply
        self.gen_histograms(self.df_replies, y_label='replies Counts',
                            title='Trend Analysis for replies',column_parm='reply_month',
                            img_name='replies_bar_chart')

        self.gen_distribution_plot(self.df_replies.reply_month, y_label='comments Counts',
                                   title='Trend Analysis for replies', img_name='replies_dist_chart')
