import threading
import praw
from datetime import datetime
import logging




class RedditSentimentWorker(threading.Thread):
    
    def __init__(self, sentiment_model, environment_variable_helper, live_data):
        
        super(RedditSentimentWorker, self).__init__()
        
        self.sentiment_model = sentiment_model

        self.target_subreddit = environment_variable_helper.get_target_subreddit()
        self.reddit_client = praw.Reddit(**environment_variable_helper.get_reddit_api_credentials())

        self.live_data = live_data
	


    def run(self):

        for comment in self.reddit_client.subreddit(self.target_subreddit).stream.comments(skip_existing=True):      
            try:
                score = self.sentiment_model.predict(comment.body)
                self.live_data.append(score,comment.body[:140])
            except Exception as e:
                logging.exception(e)
                logging.warning("Model Error")
