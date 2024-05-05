import io
import os
import certifi
import pandas as pd
import requests
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()

# Download the CSV file
response = requests.get(os.getenv("TELEGRAM_URL"))
response.raise_for_status()  # This will raise an exception if there was a download error

# Convert CSV data to DataFrame
data = pd.read_csv(io.StringIO(response.text))

# Convert DataFrame to JSON (list of dictionaries)
json_data = data.to_dict(orient='records')

# Connect to MongoDB (adjust the connection string as necessary)
client = MongoClient(os.getenv("MONGO_URL"), tlsCAFile=certifi.where(), connectTimeoutMS=50000, socketTimeoutMS=50000)
db = client['telegram']  # Specify the database name
collection = db['data']  # Specify the collection name

# Insert the JSON data into MongoDB
collection.insert_many(json_data)

print("Data successfully inserted into MongoDB.")
