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

from bson import ObjectId
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain_openai import ChatOpenAI

import asyncio
from tqdm import tqdm


# # Main for creating caches
import uvicorn

from fastapi.middleware.cors import CORSMiddleware

from datetime import datetime
 
app = FastAPI()
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
            events_to_process = events[:6]
            results = list(tqdm(executor.map(process_event, events_to_process), total=len(events_to_process)))
        with open(cache_file, 'wb') as f:
            pickle.dump(results, f)

    for result in results:
        result["_id"] = str(result["_id"])
        for event in result["telegram_posts"]:
            event["_id"] = str(event["_id"])
        # print(result)

    return results

        
@app.post("/insights")
async def insights(id):

    # Convert the provided id to an ObjectId
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

    return {"insights": result}


@app.post("/update")
async def update(request):
    data = await request.json()
    object_id = ObjectId(data['id'])
    query = data['query']
    existing_description = data['existing_description']

    # Fetch the event data from the MongoDB collection
    event_data = mongo.client['events']['data'].find_one({"_id": object_id})

    if not event_data:
        raise HTTPException(status_code=404, detail="Event not found")
    
    PROMPT = ChatPromptTemplate.from_template(f"""Given this description, and a query, update accordingly to answer the users questions. 
                                                Query: {query}
                                                Existing Description: {existing_description}
                                                Updated Description: [output here]
                                              """)
    chain = PROMPT | ChatOpenAI() | StrOutputParser()

    new_description = chain.invoke({"query": query, "existing_description": existing_description})
    # Update the event description in the MongoDB collection
    update_result = mongo.client['events']['data'].update_one(
        {"_id": object_id},
        {"$set": {"description": existing_description}}
    )

    if update_result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Update failed or no changes made")
    
    return update_result


@app.post("/correlations")
async def correlations(ids: List[str]):

    # Convert the provided id to an ObjectId
    object_ids = [ObjectId(id) for id in ids]

    # Fetch the event data from the MongoDB collection
    event_data_list = [mongo.db['events'].find_one({"_id": obj_id}) for obj_id in object_ids]

    contexts = [{"id": str(event_data["_id"]), "context": "\n".join(event_data.get('context', []))} for event_data in event_data_list if event_data]
    # Joining each context with a heading
    formatted_contexts = []
    for index, context in enumerate(contexts, start=1):
        heading = f"event {index}: "
        formatted_context = heading + context['context']
        formatted_contexts.append(formatted_context)

    combined_context = "\n".join(formatted_contexts)


    if not contexts:
        raise HTTPException(status_code=404, detail="No context available for insights generation")

    PROMPT = ChatPromptTemplate.from_template(f"""
You are a highly intelligent assistant. Your task is to analyze a list of events and identify pairs of events that have a strong causation based on their context. Your analysis should be thorough, detailing how one event directly leads to or causes another event. Provide detailed background information and specific facts that help explain the causal relationships.

### Example 1
Events:
1. Event 1: Russia mobilizes over 100,000 troops near Ukraine's eastern border.
2. Event 2: Ukraine increases border security and seeks military aid from Western allies.
3. Event 3: NATO convenes an emergency meeting, expressing deep concerns over the potential escalation of conflict.

Causal Relationship:
Event 1 strongly caused Event 3 because the unprecedented mobilization of over 100,000 Russian troops created widespread fears of an impending invasion. This large-scale military buildup prompted Ukraine to reinforce its defenses, call up reserves, and urgently seek international support. The increased tensions and looming threat of conflict spurred NATO to convene an emergency meeting, during which member states reaffirmed their commitment to supporting Ukraine's sovereignty, emphasizing collective security in the face of potential aggression.

### Example 2
Events:
1. Event 1: Ukraine introduces mandatory conscription in response to growing security concerns.
2. Event 2: NATO launches Operation Defender Europe, a series of military exercises involving 26 nations.
3. Event 3: Russia counters with Zapad 2023, its own military exercises involving tens of thousands of troops and heavy weaponry.

Causal Relationship:
Event 1 strongly caused Event 3 because Ukraine's move to introduce mandatory conscription was seen as a response to increasing regional tensions and potential military threats. NATO's subsequent launch of Operation Defender Europe further heightened concerns, as it involved military drills across Eastern Europe to demonstrate unity and readiness. In reaction to these developments, Russia launched Zapad 2023, a show of force with tens of thousands of troops, armored vehicles, and advanced missile systems, underscoring its readiness to respond to perceived provocations and showcasing its military might.

### Example 3
Events:
1. Event 1: A sophisticated cyberattack targets Ukraine's power grid, leading to widespread blackouts in major cities.
2. Event 2: Ukraine accuses Russian-backed hackers of orchestrating the attack.
3. Event 3: The United States and European Union impose strict economic sanctions on Russia, targeting key sectors of its economy.

Causal Relationship:
Event 1 strongly caused Event 3 because the cyberattack that crippled Ukraine's power grid demonstrated a high level of sophistication, pointing to state-backed actors. Ukrainian officials directly implicated Russian hackers, citing previous attacks and similarities in tactics. The international community viewed this attack as an escalation in hybrid warfare, leading the United States and European Union to impose severe economic sanctions targeting Russia's financial, energy, and defense sectors. These sanctions were meant to hold Russia accountable for actions deemed destabilizing to regional security and international norms.

### Example 4
Events:
1. Event 1: Russia announces the annexation of Crimea following a disputed referendum.
2. Event 2: The international community condemns the move, calling it a violation of Ukraine's territorial integrity.
3. Event 3: The United Nations General Assembly passes a resolution affirming Ukraine's sovereignty and rejecting Russia's annexation.

Causal Relationship:
Event 1 strongly caused Event 3 because Russia's announcement of the annexation of Crimea came after a highly controversial referendum, which was not internationally recognized and was conducted under military occupation. The annexation drew immediate condemnation from the international community, with many nations viewing it as a violation of Ukraine's territorial integrity. This led to the United Nations General Assembly passing Resolution 68/262, which affirmed Ukraine's sovereignty, recognized Crimea as part of Ukraine, and rejected the legality of Russia's actions. This resolution was an attempt to reaffirm international norms and discourage similar actions in the future.

### Your Input
Events:
{context}

Causal Relationship:
[Provide the causal relationship based on the above events]



""")
    # Use the context to generate insights using GPT
    insights = PROMPT | ChatOpenAI() | StrOutputParser()

    result = insights.invoke({"context": context})

    return {"insights": result}

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
