import io
import os
import certifi
import pandas as pd
import requests
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()
import json

# UPLOADING EVENTS
with open("backend/aggregated_events.json", "r") as f:
    results = json.load(f)

results = [
    {
        "event": event["event"],
        "location": event["location"],
        "context": event["context"],
        "time": time,
        "ids": ids,
        "embedding": event["embed"]
    } for event, time, ids in results
]

print(results[0])

# Connect to MongoDB (adjust the connection string as necessary)
client = MongoClient(os.getenv("MONGO_URL"), tlsCAFile=certifi.where(), connectTimeoutMS=50000, socketTimeoutMS=50000)
# db = client['telegram']  # Specify the database name
# collection = db['data']  # Specify the collection name
db = client['events']
collection = db['data']

# print("Results is: ", results)

# Insert the JSON data into MongoDB
collection.insert_many(results)

print("Data successfully inserted into MongoDB.")
