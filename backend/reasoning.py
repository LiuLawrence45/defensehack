from llm import LLM
from PROMPTS import *
import json

def reason(events):
    llm = LLM()
    events = "\n".join(json.encode(events))
    llm.predict(PROMPT_REASONING.format(context=events))

