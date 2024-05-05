# db_client.py
'''
Client template - brainstorm of possible features
'''

import os
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()

class MongoDBClient:
    def __init__(self, dbname="social_media_analysis", uri=os.getenv("MONGO_URL")):
        self.client = MongoClient(uri)
        try: 
            client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)
        self.db = self.client[dbname]

    def insert_telegram_message(self, message):
        """Insert a single message into the Telegram collection."""
        self.db.telegram_messages.insert_one(message)

    def find_telegram_messages_by_keyword(self, keyword):
        """Retrieve messages containing a specific keyword."""
        return list(self.db.telegram_messages.find({"message": {"$regex": keyword, "$options": "i"}}))

    def insert_tweet(self, tweet):
        """Insert a single tweet into the Twitter collection."""
        self.db.twitter_tweets.insert_one(tweet)

    def find_tweets_by_keyword(self, keyword):
        """Retrieve tweets containing a specific keyword."""
        return list(self.db.twitter_tweets.find({"text": {"$regex": keyword, "$options": "i"}}))

# Example usage
if __name__ == "__main__":
    client = MongoDBClient(dbname = "telegram")
    client.insert_telegram_message({"user_id": "12345", "message": "Example message about an event", "date": "2023-10-01"})
    client.insert_tweet({"user_id": "67890", "text": "Tweet about the same event", "date": "2023-10-01"})
    print(client.find_telegram_messages_by_keyword("event"))
    print(client.find_tweets_by_keyword("event"))
