from llm import LLM 
from datetime import datetime
from twitter_q import TwitterSearchClient
from typing import List
from PROMPTS import *

class Agent:

    def __init__(self, llm: LLM):
        self.llm = llm
        self.twitter_client = TwitterSearchClient()

    def run(self, prompt: str) -> str:
        return self.llm.generate_response(prompt)
    
    def generate_and_search_tweets(self, context: List, start_datetime: datetime, end_datetime: datetime, num_tweets_per_keyword=20):
        # Generate keywords using the LLM
        context = "\n".join(context)
        keywords_prompt = TWITTER_PROMPT.format(context=context)
        keywords = self.llm.predict_structured(keywords_prompt, schema=list)
        # Initialize TwitterSearchClient
        twitter_client = TwitterSearchClient()
        # Collect tweets for each keyword
        all_tweets = {}
        for keyword in keywords:
            tweets = twitter_client.search(start_datetime, end_datetime, keyword, num_tweets=num_tweets_per_keyword)
            all_tweets[keyword] = tweets

        return all_tweets
    
    def analyze_tweets(self, tweets: List, context: List):
        from concurrent.futures import ThreadPoolExecutor

        def analyze_tweet(tweet, context):
            context = "\n".join(context)
            analysis_prompt = TWITTER_ANALYSIS.format(tweet=tweet.text, context=context)
            return tweet if self.llm.predict_structured(analysis_prompt, schema=bool) else None

        with ThreadPoolExecutor() as executor:
            relevant_tweets = list(filter(None, executor.map(analyze_tweet, tweets, context)))

        return relevant_tweets
    
    def run_search(self, context: List, start_datetime: datetime, end_datetime: datetime, num_tweets_per_keyword=10):
        tweets = self.generate_and_search_tweets(context, start_datetime, end_datetime, num_tweets_per_keyword)
        relevant_tweets = self.analyze_tweets(tweets, context)
        return relevant_tweets



