import os
from dotenv import load_dotenv
load_dotenv()

class EnvironmentVariableHelper:

    _client_id = os.environ["CLIENT_ID"]
    _client_secret = os.environ["CLIENT_SECRET"]
    _password = os.environ["PASSWORD"]
    _user_agent = os.environ["USER_AGENT"]
    _username = os.environ["USERNAME"]

    _target_subreddit = os.environ["TARGET_SUBREDDIT"]



    def get_reddit_api_credentials(self):
        return {"client_id": self._client_id,
                "client_secret": self._client_secret,
                "password": self._password,
                "user_agent": self._user_agent,
                "username": self._username}

    def get_target_subreddit(self):
        return self._target_subreddit
