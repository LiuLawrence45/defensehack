from fastapi import FastAPI, HTTPException
from typing import List
from pydantic import BaseModel
from query import query

from src.retrieval.client import MongoDBClient
import motor.motor_asyncio
import os
import certifi

app = FastAPI()
mongo = MongoDBClient()


class SearchRequest(BaseModel):
    query: str

@app.post("/search")
async def search(request: SearchRequest):
    query_to_run = query(request.query)
    query_dict = query_to_run.__dict__
    
    results = mongo.search_telegram(search_query = query_dict["topic"], start_time = query_dict["start_date"], end_time = query_dict["end_date"])

    if not results:
        raise HTTPException(status_code=404, detail="No results found")
    return results

# if __name__ == "__main__":
#     query_to_run = query("recent events dk300 bombing with tanks in south russia")
#     query_dict = query_to_run.__dict__
#     # print("Type of query_to_run:", type(query_to_run))
#     print("Query is: ", query_dict)
#     print(mongo.search_telegram(search_query = query_dict["topic"], start_time = query_dict["start_date"], end_time = query_dict["end_date"]))

#     # location = query_dict["location"]