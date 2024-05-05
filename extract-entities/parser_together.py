from langchain_together import Together
from langchain.prompts import ChatPromptTemplate
from langchain.schema.output_parser import StrOutputParser
from prompts import ENTITY_PROMPT
import dotenv

import json 
dotenv.load_dotenv()

class Parser():
    # Extract
    @staticmethod
    def extract_events(content: str) -> dict:
        llm = Together(
            model="meta-llama/Llama-3-70b-chat-hf",
            temperature=0.7,
            max_tokens=128,
            top_k=1,
            together_api_key="7a643e3103b3a8cb676bd9d55a4d36ae9488240cb98c6794f7cfdad34f0906ee"
        )
        chain = ChatPromptTemplate.from_template(ENTITY_PROMPT) | llm | StrOutputParser()
        events = chain.invoke({
            "content": content
        })

        events = events[events.index('['):events.rindex(']')+1]
        try:
            loaded_events = json.loads(events)
        except:
            print(events)

        # for event in events:
        #     geolocator = Nominatim(user_agent="yourmomisfataf")
        #     location = geolocator.geocode(event["location"])
        #     if location:
        #         event["coordinates"] = (location.latitude, location.longitude)
        #     else:
        #         event["coordinates"] = (None, None)
        return loaded_events




