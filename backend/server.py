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

app = FastAPI()
# mongoClient = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
# mongo = MongoDBClient(mongoClient)
mongo = MongoDBClient()

agent = Agent()

class SearchRequest(BaseModel):
    query: str

@app.post("/search")
async def search(request: SearchRequest):
    query_to_run = query(request.query)
    query_dict = query_to_run.__dict__
    results = mongo.search_telegram(search_query = query_dict["topic"], start_time = query_dict["start_date"], end_time = query_dict["end_date"]) # gets us a list of events
    final_results = []
    for event in results:
        event["_id"] = str(event["_id"])
        event = agent.extract_event(data)
        context  = [
            f"Event details: {event['title']}",
            f"Event description: {" ".join(event['context'])}"
            # "Event details: An assault group of fagots was destroyed in the village of #Pervomaiskoye, through the lens of the operator of the 11th separate motorized infantry battalion “Kievan Rus”🔥💥💪🇺🇦",
            # # "Event description: ​🇷🇺⚡️Limansky and Seversky directions, situation at 13:00 March 31, 2024 On the Limansky direction at the turn of Terny - Yampolovka there are oncoming battles. The RF Armed Forces and the Ukrainian Armed Forces are trying to knock each other out of their positions. Units of the Russian Army have not yet managed to build on their success and enter the village of Terny."
        ]
        event_date = datetime.strptime(event.date, '%Y-%m-%d')
        start_time = event_date - timedelta(days=1)
        end_time = event_date + timedelta(days=1)
        results = agent.run_search(context, start_time, end_time)
        relevant_tweets_list = [tweet for tweets in results.values() for tweet in tweets]
        summary = agent.summarize(context, relevant_tweets_list)
        summary = (summary[0], [x['media_url_https'] for x in summary[1]])
        final_results.append(summary)

    if not results:
        raise HTTPException(status_code=404, detail="No results found")
    return results

if __name__ == "__main__":
    query_to_run = query("recent events dk300 bombing with tanks in south russia")
    query_dict = query_to_run.__dict__
    # print("Type of query_to_run:", type(query_to_run))
    print("Query is: ", query_dict)
    print(mongo.search_telegram(search_query = query_dict["topic"], start_time = query_dict["start_date"], end_time = query_dict["end_date"]))

    # location = query_dict["location"]