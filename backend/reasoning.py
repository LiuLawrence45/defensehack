from llm import LLM
from PROMPTS import *

def reason(events):
    llm = LLM()
    for event in events:
        llm.generate_response(PROMPT_REASONING, event)

