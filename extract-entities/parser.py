from typing import List
import dotenv
import os
from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
import requests
from bs4 import BeautifulSoup
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda
from langchain_community.utilities.duckduckgo_search import DuckDuckGoSearchAPIWrapper
from langchain_community.utilities import SerpAPIWrapper
from langchain_community.tools import BraveSearch
import json
from prompts import ENTITY_PROMPT
from langchain_core.output_parsers import JsonOutputParser

import geopy
from geopy.geocoders import Nominatim
from langchain_core.pydantic_v1 import BaseModel, Field


dotenv.load_dotenv()

class Parser():
    # Extract
    @staticmethod
    def extract_events(content: str) -> dict:
        chain = ChatPromptTemplate.from_template(ENTITY_PROMPT) | ChatOpenAI() | StrOutputParser()
        events = chain.invoke({
            "content": content
        })

        events = json.loads(events)

        # for event in events:
        #     geolocator = Nominatim(user_agent="yourmomisfataf")
        #     location = geolocator.geocode(event["location"])
        #     if location:
        #         event["coordinates"] = (location.latitude, location.longitude)
        #     else:
        #         event["coordinates"] = (None, None)
        return events



