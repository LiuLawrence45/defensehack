from llm import LLM
from PROMPTS import QUERY_PROMPT
from typing import List
from langchain_core.pydantic_v1 import BaseModel
from datetime import date, datetime, time, timedelta


class Query(BaseModel):
    start_date: datetime
    end_date: datetime
    location: str
    topic: str

llm = LLM()

def query(text: str):
    prompt = QUERY_PROMPT.replace("{context}", text)
    return llm.predict_structured(prompt, Query)

