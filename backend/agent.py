from llm import LLM 
from datetime import datetime
from twitter_q import TwitterSearchClient
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
    
    def analyze_tweets(self, tweets: List[Tweet]):
        


