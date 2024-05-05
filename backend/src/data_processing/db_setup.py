# db_setup.py
import os
from dotenv import load_dotenv
from pymongo import MongoClient
load_dotenv()

def get_database():
    """ Connect to MongoDB and return a database instance. """
    # Connection URL
    client = MongoClient(os.getenv("MONGO_URL"))
    # If your MongoDB server requires authentication, connect as follows:
    # client = MongoClient('mongodb://username:password@localhost:27017/')

    try: 
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
    # return client[db]

def setup_collections(db):
    """ Define indexes and any other collection settings here. """
    # Create or get the collection
    telegram = db['data']
    twitter = db['twitter_tweets']

    # Adding a simple index to the 'date' field on both collections
    telegram.create_index([("date", 1)])
    twitter.create_index([("date", 1)])

    print("Collections are set up with indexes.")

if __name__ == "__main__":
    db = get_database()
    # setup_collections(db)
