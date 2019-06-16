"""
Configurations
"""
AGG_BY_SUB = ['submission_id', 'submission_title', 'text_aggregate']

AGG_BY_MONTH = ['year','month','text_aggregate']

SUBMISSION_COLS = ['submission_id', 'submission_date', 'submission_year',
                   'submission_month', 'submission_day', 'submission_author', 'title']

COMMENTS_COLS = ['comments_id', 'submission_id', 'comment_date', 'comment_year',
                 'comment_month', 'comment_day', 'comment_author', 'comment']

REPLIES_COLS = ['reply_id', 'comments_id', 'submission_id', 'reply_date', 'reply_year',
                'reply_month', 'reply_day', 'reply_author', 'reply']
