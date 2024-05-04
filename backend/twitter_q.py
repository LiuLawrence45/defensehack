import os
from datetime import datetime
from twikit import Client
from dotenv import load_dotenv
load_dotenv()

class TwitterSearchClient:
    def __init__(self):
        self.username = os.getenv('TWITTER_USERNAME')
        self.email = os.getenv('TWITTER_EMAIL')
        self.password = os.getenv('TWITTER_PASSWORD')
        self.client = Client('en-US')
        self.login()

    def login(self):
        cookies_path = 'cookies.json'
        try:
            self.client.load_cookies(cookies_path)
        except FileNotFoundError:
            if not all([self.username, self.email, self.password]):
                raise ValueError("Missing environment variables for Twitter credentials")
            self.client.login(auth_info_1=self.username, auth_info_2=self.email, password=self.password)
            self.client.save_cookies(cookies_path)

    def search(self, start_datetime, end_datetime, query, num_tweets=20):
        if not isinstance(start_datetime, datetime) or not isinstance(end_datetime, datetime):
            raise ValueError("start_datetime and end_datetime must be datetime objects")
        formatted_start_date = start_datetime.strftime('%Y-%m-%d')
        formatted_end_date = end_datetime.strftime('%Y-%m-%d')
        search_query = f'until:{formatted_end_date} since:{formatted_start_date} {query}'
        
        tweets = []
        result = self.client.search_tweet(search_query, 'Latest', count=min(num_tweets, 20))
        tweets.extend(result)
        count = 0
        while count < num_tweets:
            more_tweets = result.next()  # Retrieve more tweets
            tweets.extend(more_tweets[:max(0, num_tweets - count)])
            count += 20

        return tweets
    
    def get_tweet_by_id(self, tweet_id):
        try:
            tweet = self.client.get_tweet_by_id(tweet_id)
            return tweet
        except Exception as e:
            print(f"An error occurred while fetching the tweet: {e}")
            return None
