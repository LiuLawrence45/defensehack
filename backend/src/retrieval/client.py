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

load_dotenv()

class MongoDBClient:
    def __init__(self, uri=os.getenv("MONGO_URL")):
        self.client = MongoClient(uri)
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
    
    def search(self, dbName, collectionName):
        collection = self.client[dbName][collectionName]

        # item_details = collection.find()
        category_index = collection.create_index("category")

        try:
            results = collection.find({"translation": "air conditioner"})
            return list(results)
        
        except Exception as e:
            print("Error occurred: ", e)

        


# Example usage
if __name__ == "__main__":
    client = MongoDBClient()
    client.search("telegram", "data")
    # client.search("telegram", "data");

