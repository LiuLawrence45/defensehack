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

    telegram_posts = []
    for event in events:
        for id in event["ids"]:
            post = mongo.search_telegram_id(id)
            if post is not None:
                telegram_posts.append(post)

    print("Telegram Posts:")
    for post in telegram_posts:
        print("#" * 50)
        print(post)
    print("#" * 50)



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

if __name__ == "__main__":

    async def main():
        events = await mongo_one("What has happened with Kyiv in Ukraine?")
        telegram_posts = []
        for event in events:
            event['posts'] = []
            for id in event["ids"]:
                post = mongo.search_telegram_id(id)
                if post is not None:
                    telegram_posts.append(post)
                    event['posts'].append(post)

        
    asyncio.run(main())

# if __name__ == "__main__":
    # query_to_run = query("over the past two months dk300 bombing with tanks in south russia")

    # chain = ChatPromptTemplate.from_template(QUERY_PROMPT) | ChatOpenAI() | StrOutputParser()
    # result = chain.invoke({"context": "What has happened with SP300 missles in Ukraine?", "date": datetime.now().strftime("%Y-%m-%d")})
    # try:
    #     query_dict = json.loads(result)
    #     print("Valid JSON:", query_dict)
    # except json.JSONDecodeError:
    #     print("Invalid JSON received from chain.invoke")
    # location = gmaps.geocode(query_dict["location"])
    
    # try: 
    #     loc = (location[0]['geometry']['location']['lat'], location[0]['geometry']['location']['lng'])
    #     # print("Location is: ", location)
    # except Exception as e:
    #     print("Reached error: ", e)
    #     loc = None

    # print("Start time: ", query_dict["start_date"])
    # print("End time", query_dict["end_date"])
    # results = mongo.search_events(start_time = datetime.fromisoformat(query_dict["start_date"]), end_time = datetime.fromisoformat(query_dict["end_date"]), coordinates = loc) # gets us a list of events
    # for result in results:
    #     print("Content: ", result["event"])
    #     print("\nTime: ", result["time"])
    #     print("\nLocation: ", result["location"])
    #     print("#"*50)

    # final_results = []
    # for event in results[1:2]:
    #     event["_id"] = str(event["_id"])
    #     context  = [
    #         f"Event details: {event['event']}",
    #         f"Event description: {" ".join(event['context'])}"
    #     ]
    #     event_date = datetime.fromisoformat(event['time'])
    #     start_time = (event_date - timedelta(days=1))
    #     end_time = event_date + timedelta(days=1)
    #     results = agent.run_search(context, start_time, end_time)
    #     relevant_tweets_list = [tweet for tweets in results.values() for tweet in tweets]
    #     summary = agent.summarize(context, relevant_tweets_list)
    #     summary = (summary[0], [x['media_url_https'] for x in summary[1]], event['time'], event['location'])
    #     final_results.append(summary)

    # print(final_results)

    # for result in results:
    #     print(result.keys())
    #     print("*"*50)

    # location = query_dict["location"]