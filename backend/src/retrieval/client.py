import os
from pymongo import MongoClient
from dotenv import load_dotenv

from langchain_openai import OpenAIEmbeddings
from langchain_openai import OpenAI
from langchain_mongodb import MongoDBAtlasVectorSearch

import os
from pymongo import MongoClient
from dotenv import load_dotenv
from pandas import DataFrame
from datetime import datetime, timedelta
import json

load_dotenv()

class MongoDBClient:

    def __init__(self, client = MongoClient(os.getenv("MONGO_URL"))):
        self.client = client
        self.telegram = self.client["telegram"]
        try: 
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)

    def vectorSearch(self, dbName, collectionName, index_name) -> MongoDBAtlasVectorSearch:
        vector_search = MongoDBAtlasVectorSearch.from_connection_string(
        os.getenv("MONGO_URL"),
        dbName + "." + collectionName,
        OpenAIEmbeddings(disallowed_special=()),
        index_name=index_name
        )
        return vector_search

    def search_telegram(self, search_field="description", search_query="", start_time=None, end_time=None) -> str:
        collection = self.client["telegram"]["data"]

        # Create index for the search field and time
        collection.create_index([(search_field, 1), ("time", 1)])

        # Query is a dict, with the keys = to fields in each object in MongoDB
        query = {}

        # If a search query is provided, add as a key.
        if search_query:
            query[search_field] = search_query

        # # If time range is not provided, default to the past two weeks
        if not start_time or not end_time:
            end_time = datetime.now()
            start_time = end_time - timedelta(weeks=2)


        query["time"] = {"$gte": start_time, "$lte": end_time}

        print("Query is: ", query)

        try:
            results = collection.find(query)
            for result in results:
                print(result["time"])
            return list(results)
        
        except Exception as e:
            print("Error occurred: ", e)

        


# Example usage
if __name__ == "__main__":
    client = MongoDBClient()
    start_time = "2024-03-31 00:00:00"
    end_time = "2024-03-31 23:59:59"   
    print(client.search_telegram(start_time = start_time, end_time = end_time))

