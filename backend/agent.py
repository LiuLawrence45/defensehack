from llm import LLM 
from datetime import datetime
from twitter_q import TwitterSearchClient
from typing import List
from PROMPTS import *
from pydantic import BaseModel, Field

class Agent:

    def __init__(self):
        self.llm = LLM()
        self.twitter_client = TwitterSearchClient()
        print("Agent initialized with LLM and TwitterSearchClient.")

    def run(self, prompt: str) -> str:
        response = self.llm.generate_response(prompt)
        print(f"Generated response for the prompt: {prompt}")
        return response
    
    def generate_and_search_tweets(self, context: List, start_datetime: datetime, end_datetime: datetime, num_tweets_per_keyword=10):
        # Generate keywords using the LLM
        context = "\n".join(context)
        keywords_prompt = TWITTER_PROMPT.format(context=context)
        class TL(BaseModel):
            keywords: List[str] = Field(..., description="List of keywords to be used for Twitter search.")

        print(f"Generating keywords for context: {context}")
        keywords = self.llm.predict_structured(keywords_prompt, schema=TL)
        print(f"Generated keywords: {keywords.keywords}")
        # Initialize TwitterSearchClient
        twitter_client = TwitterSearchClient()
        # Collect tweets for each keyword
        all_tweets = {}
        for keyword in keywords.keywords:
            print(f"Searching for tweets with keyword: {keyword}")
            tweets = twitter_client.search(start_datetime, end_datetime, keyword, num_tweets=num_tweets_per_keyword)
            all_tweets[keyword] = tweets
            print(f"Found {len(tweets)} tweets for keyword: {keyword}")

        return all_tweets
    
    def analyze_tweets(self, tweets: List, context: List):
        from concurrent.futures import ThreadPoolExecutor

        def analyze_tweet(tweet, context):
            try:
                context = "\n".join(context)
                analysis_prompt = TWITTER_ANALYSIS.format(tweet=tweet.text, context=context)
                class TweetAnalysisResult(BaseModel):
                    relevant: bool = Field(..., description="Determines if the tweet is relevant to the context.")
                result = self.llm.predict_structured(analysis_prompt, schema=TweetAnalysisResult)
                return tweet if result.relevant else None
            except Exception as e:
                print(f"An error occurred while analyzing tweet: {tweet.text}. Error: {e}")
                return None

        with ThreadPoolExecutor() as executor:
            print("Analyzing tweets in parallel.")
            relevant_tweets = list(filter(None, executor.map(analyze_tweet, tweets, [context]*len(tweets))))
            print(f"Found {len(relevant_tweets)} relevant tweets.")

        return relevant_tweets
    
    def run_search(self, context: List, start_datetime: datetime, end_datetime: datetime, num_tweets_per_keyword=10):
        print("Running search for tweets.")
        tweets = self.generate_and_search_tweets(context, start_datetime, end_datetime, num_tweets_per_keyword)
        relevant_tweets = {}
        for keyword, tweets_list in tweets.items():
            relevant_tweets[keyword] = self.analyze_tweets(tweets_list, context)
        print("Search completed.")
        return relevant_tweets
    
    def summarize(self, context, tweets: List):
        # Join all tweet texts into a single string separated by newlines
        context_joined = "\n".join(context)
        tweet_texts = "\n".join([tweet.text.replace('\n', ' ') for tweet in tweets])
        media = []
        for tweet in tweets:
            if hasattr(tweet, 'media') and tweet.media:
                media.extend(tweet.media)
        summary_prompt = SUMMARIZE.format(context=context_joined, data=tweet_texts)
        print(summary_prompt)
        summary_result = self.llm.predict(summary_prompt)
        return (summary_result, media)
    
    def extract_event(self, context: List):
        context_joined = "\n".join(context)
        event_prompt = EXTRACT_EVENT.format(context=context_joined)
        print(event_prompt)
        event_result = self.llm.predict(event_prompt)
        return event_result
