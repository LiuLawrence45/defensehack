from fastapi import FastAPI, HTTPException
from typing import List
from pydantic import BaseModel
from query import query
from agent import Agent
from datetime import datetime, timedelta
from src.retrieval.client import MongoDBClient
import motor.motor_asyncio
import os
import certifi
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain_openai import ChatOpenAI
import json
import hashlib
import pickle
import time
import random

from datetime import datetime
 
app = FastAPI()
# mongoClient = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
# mongo = MongoDBClient(mongoClient)
mongo = MongoDBClient()

agent = Agent()

class SearchRequest(BaseModel):
    query: str

import googlemaps
gmaps = googlemaps.Client(key='AIzaSyDcGkvKU23hRBD5LBmxaOTT2A-2NT4mCk8')

QUERY_PROMPT = """
Given a natural language query, decompose the query into a structured query object with the following fields:

start_date: datetime
end_date: datetime
location: str
topic: str

If not start/end date is passed, return the past year. Today is {date}

For example, given this query:

Find everything happening in Ukraine over the past 2 days

Return:
{{

"start_date": "2024-02-28T00:00:00.000Z",
"end_date": "2024-03-01T00:00:00.000Z",
"location": "Ukraine",
"topic": "ukraine",
}}


Given this query:

What has happened with SP300 missles in Ukraine?

Return:
{{
"start_date": "2023-05-04T00:00:00.000Z",
"end_date": "2024-05-04T00:00:00.000Z",
"location": "Ukraine",
"topic": "sp300 missiles",

}}


Given this query:

{context}

Return, in valid JSON output:

"""
    # query_dict = query_to_run.__dict__
chain = ChatPromptTemplate.from_template(QUERY_PROMPT) | ChatOpenAI() | StrOutputParser()

# Fetching all events from mongo_one.
async def mongo_one(query) -> List:

    result = chain.invoke({"context": query, "date": datetime.now().strftime("%Y-%m-%d")})
    try:
        query_dict = json.loads(result)
        print("Valid JSON:", query_dict)
    except json.JSONDecodeError:
        print("Invalid JSON received from chain.invoke")
        substitute = ChatPromptTemplate.from_template("Reformat the following query into valid JSON: {query}") | ChatOpenAI() | StrOutputParser()
        result = substitute.invoke({str(result)})
        try:
            query_dict = json.loads(result)
        except Exception as e:
            print("YOURE DONE FOR.")
    

    location = gmaps.geocode(query_dict["location"])
    
    try: 
        loc = (location[0]['geometry']['location']['lat'], location[0]['geometry']['location']['lng'])
    except Exception as e:
        print("Reached error fetching location from GMAPS!!: ", e)
        loc = None

    results = mongo.search_events(start_time = datetime.fromisoformat(query_dict["start_date"]), end_time = datetime.fromisoformat(query_dict["end_date"]), coordinates = loc) 
    return results


@app.post("/search")
async def search(request: SearchRequest):
    events = await mongo_one(request.query)

    # Calculate the MD5 hash of the query string
    query_hash = hashlib.md5(request.query.encode('utf-8')).hexdigest()
    print(f"MD5 hash of the query: {query_hash}")
    from concurrent.futures import ThreadPoolExecutor


    def process_event(event):
        time.sleep(random.randint(1, 3))
        event['telegram_posts'] = []
        event.pop('embedding', None)

        # Add telegram logs
        for id in event["ids"]:
            post = mongo.search_telegram_id(id)
            if post is not None:
                event['telegram_posts'].append(post)

        event['twitter_posts'] = []
        # Add twitter posts
        context = [
            f"Event details: {event['event']}",
            f"Event description: {' '.join(event['context'])}"
        ]
        event_date = datetime.fromisoformat(event['time'])
        start_time = event_date - timedelta(days=1)
        end_time = event_date + timedelta(days=1)
        try:
            results = agent.run_search(context, start_time, end_time)
            relevant_tweets_list = [tweet for tweets in results.values() for tweet in tweets]
        except Exception as e:
            print("Error while fetching relevant tweets: ", e)
            relevant_tweets_list = []
        summary = agent.summarize(context, relevant_tweets_list)
        summary = (summary[0], [x['media_url_https'] for x in summary[1]], event['time'], event['location'])
        event['twitter_posts'].append(summary)
        print(event)
        return event

    cache_file = f'cache/{query_hash}.pkl'
    if os.path.exists(cache_file):
        with open(cache_file, 'rb') as f:
            results = pickle.load(f)
    else:
        with ThreadPoolExecutor() as executor:
            events_to_process = events[:4]
            results = list(tqdm(executor.map(process_event, events_to_process), total=len(events_to_process)))
        with open(cache_file, 'wb') as f:
            pickle.dump(results, f)

    for result in results:
        result["_id"] = str(result["_id"])
        for event in result["telegram_posts"]:
            event["_id"] = str(event["_id"])
        # print(result)

    return results

        

from bson import ObjectId
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain_openai import ChatOpenAI
@app.post("/insights")
async def insights(id):

    # Convert the provided id to an ObjectId
    object_id = ObjectId(id)

    # Fetch the event data from the MongoDB collection
    event_data = mongo.db['events'].find_one({"_id": object_id})

    if not event_data:
        raise HTTPException(status_code=404, detail="Event not found")

    # Extract the context from the event data
    context = "\n".join(event_data.get('context', []))


    if not context:
        raise HTTPException(status_code=404, detail="No context available for insights generation")

    PROMPT = ChatPromptTemplate.from_template("From the following facts, generate very meaningful insights that a command officer or intel officer could use. Pretend you are sherlock holmes and you are trying to optimize the safety of the united states. Each insight should be an element in an array. You will return an array formatted like this. [insight 1, insight 2, insight 3]. Remember this format. These insights should be pretty long paragraphs. Here is the context: {context}")
    # Use the context to generate insights using GPT
    insights = PROMPT | ChatOpenAI() | StrOutputParser()

    result = insights.invoke({"context": context})

    return {"insights": result}


    # # Twitter parsing
    # final_results = []
    # for event in results[:10]:
    #     event["_id"] = str(event["_id"])
    #     context  = [
    #         f"Event details: {event['title']}",
    #         f"Event description: {" ".join(event['context'])}"
    #     ]
    #     event_date = datetime.strptime(event.date, '%Y-%m-%d')
    #     start_time = event_date - timedelta(days=1)
    #     end_time = event_date + timedelta(days=1)
    #     results = agent.run_search(context, start_time, end_time)
    #     relevant_tweets_list = [tweet for tweets in results.values() for tweet in tweets]
    #     summary = agent.summarize(context, relevant_tweets_list)
    #     summary = (summary[0], [x['media_url_https'] for x in summary[1]], event['date'], event['location'])
    #     final_results.append(summary)
    # print(final_results)


    # if not final_results:
    #     raise HTTPException(status_code=404, detail="No results found")
    # return final_results

import asyncio
from tqdm import tqdm


# # Main for creating caches
import uvicorn

if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8080, reload=True)


#     async def main():
#         events = await mongo_one("over the past two months dk300 bombing with tanks in south russia")
#         for i, event in enumerate(tqdm(events)):
#             event.pop("embedding", None)
#             event['telegram_posts'] = []

#             # Add telegram logs
#             for id in event["ids"]:
#                 post = mongo.search_telegram_id(id)
#                 if post is not None:
#                     post.pop("body", None)
#                     event['telegram_posts'].append(post)

#             event['twitter_posts'] = []


#             # Add twitter posts
#             # if (len(event['telegram_posts']) > 2 and i < 10):
#             #     context  = [
#             #         f"Event details: {event['event']}",
#             #         f"Event description: {" ".join(event['context'])}"
#             #     ]
#             #     event_date = datetime.fromisoformat(event['time'])
#             #     start_time = event_date - timedelta(days=1)
#             #     end_time = event_date + timedelta(days=1)
#             #     results = agent.run_search(context, start_time, end_time)
#             #     relevant_tweets_list = [tweet for tweets in results.values() for tweet in tweets]
#             #     summary = agent.summarize(context, relevant_tweets_list)
#             #     summary = (summary[0], [x['media_url_https'] for x in summary[1]], event['time'], event['location'])
#             #     event['twitter_posts'].append(summary)

#         with open("results/CACHE_1_nontwitter.json", "w") as f:
#             json.dump(events, f, default=str, indent = 4)
#             print("SAVED!@!!")

#     asyncio.run(main())


# # if __name__ == "__main__":
# #     id = "66378096b1b563eb4d670d5c"
# #     object_id = ObjectId(id)

# #     # Fetch the event data from the MongoDB collection
# #     event_data = mongo['events']['data'].find_one({"_id": object_id})

# #     if not event_data:
# #         raise HTTPException(status_code=404, detail="Event not found")

# #     # Extract the context from the event data
# #     context = "\n".join(event_data.get('context', []))


# #     if not context:
# #         raise HTTPException(status_code=404, detail="No context available for insights generation")

# #     PROMPT = ChatPromptTemplate.from_template("From the following facts, generate very meaningful insights that a command officer or intel officer could use. Pretend you are sherlock holmes and you are trying to optimize the safety of the united states. Each insight should be an element in an array. You will return an array formatted like this. [insight 1, insight 2, insight 3]. Remember this format. These insights should be pretty long paragraphs. Here is the context: {context}")
# #     # Use the context to generate insights using GPT
# #     insights = PROMPT | ChatOpenAI() | StrOutputParser()

# #     result = insights.invoke({"context": context})

# #     print({"insights": result})
