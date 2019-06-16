"""
Step 1: Data wrangling:
- Extract data from Reddit using the PRAW library
"""
import praw
from datetime import datetime


class RedditWrangler:
    def __init__(self):
        # defining wrapper object
        self.reddit_wrapper = praw.Reddit(client_id='98vLAKPv_wZ84g',
                                     client_secret='JmIlMu11ULstnyGPUpTdaaO498k',
                                     user_agent='travel_subreddit')

        # schema for submissions/comments/replies data
        # TODO: Replace by Config variables
        self.submission_schema = ['submission_id', 'submission_date', 'submission_year', 'submission_month',
                                  'submission_day', 'submission_author', 'title']

        self.comment_schema = ['comments_id', 'submission_id', 'comment_date', 'comment_year',
                               'comment_month', 'comment_day', 'comment_author', 'comment']

        self.replies_schema = ['reply_id', 'comments_id','submission_id', 'reply_date', 'reply_year',
                               'reply_month', 'reply_day', 'reply_author', 'reply']

    def extract_data(self, inp_sub_reddit, top_limit="year", replace_more_limit=10):
        """
        :param inp_sub_reddit: input subreddit for which the data has to be extracted
        :param top_limit:  identify which records to be looked
        :param replace_more_limit: limit of how many records to be expanded for nested comments and comments
        :return:
        """
        #print(inp_sub_reddit)
        # accessing subreddit
        #subreddit = self.reddit_wrapper.subreddit(inp_sub_reddit)
        #print(type(subreddit),inp_sub_reddit)

        # output directory:
        output_dir="../data/"+str(inp_sub_reddit)
        submission_output = output_dir + "_" + "submission.tsv"
        comments_output = output_dir + "_" + "comments.tsv"
        replies_output = output_dir + "_" + "replies.tsv"

        submssion_writer = open(submission_output, "w")
        # add schema to file
        submssion_writer.write("\t".join(self.submission_schema) + "\n")

        comment_writer = open(comments_output, "w")
        # add schema to file
        comment_writer.write("\t".join(self.comment_schema) + "\n")

        replies_writer = open(replies_output, "w")
        # add schema to file
        replies_writer.write("\t".join(self.replies_schema) + "\n")


        # ---- SUBMISSION----
        for submission in self.reddit_wrapper.subreddit(inp_sub_reddit).top(top_limit):
            # extracting date/year/month/day for submissions
            s_date = datetime.utcfromtimestamp(submission.created_utc)
            submission_data = [submission.id, s_date, s_date.year, s_date.month, s_date.day,
                               submission.author, submission.title]
            # writing record to submission file
            submssion_writer.write("{submission_values[0]}\t{submission_values[1]}\t{submission_values[2]}\t"
                                   "{submission_values[3]}\t{submission_values[4]}\t{submission_values[5]}\t"
                                   "{submission_values[6]}\n".format(submission_values=submission_data))

            # --- COMMENTS-----
            submission.comments.replace_more(limit=replace_more_limit)
            for comment in submission.comments.list():

                # extracting date/year/month/day for comments
                c_date = datetime.utcfromtimestamp(comment.created_utc)
                comment_text = ' '.join(comment.body.split('\t'))
                comment_data = [comment.id, submission.id, c_date, c_date.year, c_date.month,
                                c_date.day, comment.author, ' '.join(comment_text.split("\n"))]
                # writing record to comments file
                comment_writer.write("{comment_values[0]}\t{comment_values[1]}\t{comment_values[2]}\t"
                                     "{comment_values[3]}\t{comment_values[4]}\t{comment_values[5]}\t"
                                     "{comment_values[6]}\t{comment_values[7]}\n".
                                     format(comment_values=comment_data))

                # ------ REPLIES --------
                comment.replies.replace_more(limit=replace_more_limit)
                for reply in comment.replies.list():
                    # extracting date/year/month/day for replies
                    r_date = datetime.utcfromtimestamp(reply.created_utc)
                    replies_text = ' '.join(reply.body.split('\t'))
                    reply_data = [reply.id, comment.id, submission.id, r_date, r_date.year,
                                  r_date.month, r_date.day, reply.author, ' '.join(replies_text.split('\n'))]
                    # writing record to replies file
                    replies_writer.write("{reply_values[0]}\t{reply_values[1]}\t{reply_values[2]}\t"
                                         "{reply_values[3]}\t{reply_values[4]}\t{reply_values[5]}\t"
                                         "{reply_values[6]}\t{reply_values[7]}\t{reply_values[8]}\n".
                                         format(reply_values=reply_data))

        # close file handlers-
        submssion_writer.close()
        comment_writer.close()
        replies_writer.close()
