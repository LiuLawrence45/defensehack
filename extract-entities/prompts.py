from langchain_core.prompts import ChatPromptTemplate

ENTITY_PROMPT = ChatPromptTemplate.from_template("""

Given a string, extract all notable events mentioned. Return in a list format as such:

['event 1', 'event 2', 'event 3']

Here is the string: {string}


 """)