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
from typing import List, Tuple
load_dotenv()
from collections.abc import MutableMapping
from pymongo import GEOSPHERE

class MongoDBClient:

    def __init__(self, client = MongoClient(os.getenv("MONGO_URL"))):
        self.client = client
        # self.telegram = self.client["telegram"]
        try: 
            self.client.admin.command('ping')
            print("Pinged your deployment. You successfully connected to MongoDB!")
        except Exception as e:
            print(e)

 
    def search_telegram_id(self, id: str) -> List:
        collection = self.client["telegram"]["data"]
        collection.create_index([("id", 1)])

        try:
            results = collection.find({"id": id.strip()})
            results = list(results)
            for result in results:
                print("Result is: ", result["event"])
            print("#"*30)
            return results
        
        except Exception as e:
            return None


    # Given a query, finds relevant events. These events are all Documents, that also contain a list of ids
    def search_events(self, start_time = None, end_time = None, coordinates: Tuple = None) -> List:
        collection = self.client["events"]["data"]
        # Create index for the time. Assuming the time is going to be held in time, and embedding in embedding.
        collection.create_index([("time", 1)])
        collection.create_index([("location", "2dsphere")])

        # Query is a dict, with the keys = to fields in each object in MongoDB
        query = {}

        # # If time range is not provided, default to the past two weeks
        if start_time and end_time:
            end_time = end_time.replace(microsecond=0).isoformat()
            start_time = start_time.replace(microsecond=0).isoformat()

        if not start_time or not end_time:
            end_time = datetime.now().replace(microsecond=0).isoformat()
            start_time = (datetime.now() - timedelta(weeks=5)).replace(microsecond=0).isoformat()

        query["time"] = {"$gte": start_time, "$lte": end_time}

        # print("Query time: ", query["time"])

        if coordinates is not None:
            latitude, longitude = coordinates
            # MongoDB uses a 'near' query with GeoJSON format for location data
            # We need to convert the coordinates to GeoJSON format
            geo_json_location = {
                "type": "Point",
                "coordinates": [longitude, latitude]
            }
            # Adding a location query to find documents within 50 miles (approximately 80467 meters)
            query['location'] = {
                "$nearSphere": {
                    "$geometry": geo_json_location,
                    "$maxDistance": 80467
                }
            }
        else:
            print("COORDS ARE NOT PROVIFED")

        try:
            results = collection.find(query)
            return list(results)
        
        except Exception as e:
            print("Error occurred: ")

        # # Create a vector search instance
        # vector_search = MongoDBAtlasVectorSearch.from_connection_string(
        #     os.getenv("MONGO_URL"),
        #     "chunked.data",
        #     OpenAIEmbeddings(disallowed_special=()),
        #     index_name="vector_index"
        # )

        # embeddings = OpenAIEmbeddings().embed_text(query)
        # results = vector_search.similarity_search(embeddings, k=top_k)
        # document_ids = [result['_id'] for result in results]
        # documents = collection.find({'_id': {'$in': document_ids}})
        # return list(documents)

    # def test_geo_index(self, latitude: float, longitude: float):
    #     collection = self.client["events"]["data"]
    #     geo_json_location = {
    #         "type": "Point",
    #         "coordinates": [longitude, latitude]
    #     }
    #     query = {
    #         "location": {
    #             "$nearSphere": {
    #                 "$geometry": geo_json_location,
    #                 "$maxDistance": 100000000000  # Adjust distance in meters
    #             }
    #         }
    #     }
    #     results = collection.find(query)
    #     return list(results)

# Example usage
# if __name__ == "__main__":
#     client = MongoDBClient()
#     # results = client.test_geo_index(30, 40)
#     # for result in results:
#     #     print(result["location"])
#     start_time = "2024-03-31T00:00:00"
#     end_time = "2024-03-31T23:59:59"   
#     results = client.search_events(coordinates = (5, 5))
#     print(len(results))
#     for result in results:
#         print(result["event"], "\n", result["context"], "\nTime: ", result["time"], "\nLocation: ", result["location"])
#         print("*"*50)

