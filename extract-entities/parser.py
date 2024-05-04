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


dotenv.load_dotenv()

class Parser():
    # Extract
    @staticmethod
    def extract_events(content: str) -> dict:
        chain = ENTITY_PROMPT | ChatOpenAI() | StrOutputParser()
        print(chain.invoke({
            "string": content
        }))


if __name__ == "__main__":
    Parser.extract_events("""In Kamchatka, a formation of ships guarding the water area of the Pacific Fleet conducted training to repel an attack by conditional saboteurs.

According to the exercise scenario, conditional saboteurs entered the territory of the formation headquarters with the aim of causing sabotage and disrupting the operation of the communications system.

After receiving a signal about an attack by unknown armed persons on the checkpoint of the connection, military personnel of the anti-terrorism unit quickly responded and began working out an algorithm of actions to repel the attack and block the saboteurs.

The training was carried out in conditions as close as possible to the real situation, and simulation tools were also actively used.

More than 20 military personnel and 3 units of military equipment took part in the event.

Press service of the Eastern Military District#Kamchatka#saboteurs#PDSS#training#combat training""")



