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


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Specify the correct origins as needed
    allow_credentials=True,
    allow_methods=["*"],  # Or specify just the methods you need: ['GET', 'POST', etc.]
    allow_headers=["*"],
)

@app.post("/search")
async def search(request: SearchRequest):
    events = await mongo_one(request.query)
    for event in tqdm(events):
        event['telegram_posts'] = []
        event.pop('embedding')

        # Add telegram logs
        for id in event["ids"]:
            post = mongo.search_telegram_id(id)
            if post is not None:
                event['telegram_posts'].append(post)

        # event['twitter_posts'] = []
        # # Add twitter posts
        # context  = [
        #     f"Event details: {event['event']}",
        #     f"Event description: {" ".join(event['context'])}"
        # ]
        # event_date = datetime.fromisoformat(event['time'])
        # start_time = event_date - timedelta(days=1)
        # end_time = event_date + timedelta(days=1)
        # results = agent.run_search(context, start_time, end_time)
        # relevant_tweets_list = [tweet for tweets in results.values() for tweet in tweets]
        # summary = agent.summarize(context, relevant_tweets_list)
        # summary = (summary[0], [x['media_url_https'] for x in summary[1]], event['time'], event['location'])
        # event['twitter_posts'].append(summary)

        

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



@app.post("/correlations")
async def correlations(ids: List[str]):

    # Convert the provided id to an ObjectId
    object_ids = [ObjectId(id) for id in ids]

    # Fetch the event data from the MongoDB collection
    event_data_list = [mongo.db['events'].find_one({"_id": obj_id}) for obj_id in object_ids]

    contexts = [{"id": str(event_data["_id"]), "context": "\n".join(event_data.get('context', []))} for event_data in event_data_list if event_data]


    if not contexts:
        raise HTTPException(status_code=404, detail="No context available for insights generation")

    PROMPT = ChatPromptTemplate.from_template("From the following facts, generate very meaningful insights that a command officer or intel officer could use. Pretend you are sherlock holmes and you are trying to optimize the safety of the united states. Each insight should be an element in an array. You will return an array formatted like this. [insight 1, insight 2, insight 3]. Remember this format. These insights should be pretty long paragraphs. Here is the context: {context}")
    # Use the context to generate insights using GPT
    insights = PROMPT | ChatOpenAI() | StrOutputParser()

    result = insights.invoke({"context": context})

    return {"insights": result}

import asyncio
from tqdm import tqdm

# # Main for creating caches
# if __name__ == "__main__":

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


if __name__ == "__main__":
    id = "66378096b1b563eb4d670d5c"
    object_id = ObjectId(id)

    # Fetch the event data from the MongoDB collection
    event_data = mongo.client['events']['data'].find_one({"_id": object_id})

    if not event_data:
        raise HTTPException(status_code=404, detail="Event not found")

    # Extract the context from the event data
    context = "\n".join(event_data.get('context', []))


    if not context:
        raise HTTPException(status_code=404, detail="No context available for insights generation")

    PROMPT = ChatPromptTemplate.from_template(f"""From the following facts, generate very meaningful insights that a command officer or intel officer could use. Pretend you are sherlock holmes and you are trying to optimize the safety of the united states. Each insight should be an element in an array. You will return an array formatted like this. [insight 1, insight 2, insight 3]. Remember this format. These insights should be pretty long paragraphs. 
                                              
                                              Example: 
                                              Input: Ukrainian Armed Forces tank destroyed by direct hit from Krasnopol guided missile

                                              Output: [  "The destruction of the Ukrainian Armed Forces tank by a Krasnopol guided missile highlights the precision capabilities of artillery systems that leverage guided munitions. This suggests a significant threat to armored vehicles, requiring the US and its allies to develop or acquire advanced countermeasures, such as electronic warfare systems or counter-battery radar systems. Enhanced mobility and stealth features may also be necessary for armored vehicles to survive in such high-threat environments.",    "The successful use of the Krasnopol missile indicates that adversaries possess the ability to effectively target key military assets with high precision. This points to the need for the United States to prioritize intelligence gathering on adversary artillery capabilities, refine force positioning strategies, and enhance the survivability of key military assets through improved camouflage, concealment, and deception techniques. Developing electronic countermeasures to disrupt the missile's guidance system could also mitigate this threat.",    "The deployment of guided munitions such as the Krasnopol missile introduces new challenges in modern warfare, particularly concerning the defense of armored vehicles and fortified positions. The United States should consider increasing investments in emerging technologies, such as active protection systems that can intercept incoming missiles. Additionally, advancing drone surveillance and reconnaissance will be crucial in identifying enemy artillery positions to neutralize these threats before they can engage."]

                                              Example 2: 
                                              
                                              Input: Intelligence reports reveal that a rogue state has successfully tested a hypersonic missile capable of evading current missile defense systems.

                                                Output: [  "The successful test of a hypersonic missile by a rogue state underscores the evolving nature of global threats, particularly to the United States and its allies. This achievement demonstrates a significant advancement in missile technology, capable of evading current missile defense systems due to its speed and maneuverability. The United States must prioritize the development of next-generation missile defense systems that can effectively track and intercept these advanced threats. This includes enhancing space-based sensors and improving radar systems for better early detection of hypersonic weapons.",    "The proliferation of hypersonic missile technology among rogue states necessitates a reassessment of existing military strategies and policies. The United States needs to invest in research and development to better understand the trajectories and flight characteristics of hypersonic missiles. This can lead to the design of specialized countermeasures tailored to intercept these advanced projectiles. Enhanced diplomatic efforts should also be pursued to prevent the spread of this technology, including through arms control agreements and strategic alliances.",    "The test highlights a shift in the balance of power, with emerging threats able to challenge the technological superiority that the United States has relied upon for deterrence. Adapting to this new reality will require increased investment in emerging defense technologies and cybersecurity to protect critical systems from disruption. Furthermore, the United States must foster stronger international partnerships to ensure collective security against hypersonic threats, involving joint research initiatives and intelligence sharing to stay ahead of potential adversaries."]

                                              Now, here is the input: 
                                              Input: {context}

                                              
                                              Output: """)
    # Use the context to generate insights using GPT
    insights = PROMPT | ChatOpenAI() | StrOutputParser()

    result = insights.invoke({"context": context})

    print({"insights": result})
