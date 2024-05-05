import os
import openai
import time
from langchain_core.pydantic_v1 import BaseModel, Field, validator
from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

from dotenv import load_dotenv
load_dotenv()

class LLM:
    def __init__(self):
        self.openai_key = os.getenv('OPENAI_KEY')
        self.openai = openai.OpenAI()
        self.client = ChatOpenAI(temperature=0, model="gpt-4-turbo")

    def predict(self, prompt, model="gpt-4-turbo"):
        response = self.openai.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )
        return response.choices[0].message.content

    def predict_structured(self, prompt, schema):
        output_parser = PydanticOutputParser(pydantic_object=schema)

        format_instructions = output_parser.get_format_instructions()
        prompt_template = PromptTemplate(
            template="{prompt}\n{format_instructions}\n",
            input_variables=["prompt"],
            partial_variables={"format_instructions": format_instructions},
        )

        model = self.client
        chain = prompt_template | model | output_parser
        result = chain.invoke({"prompt": prompt})
        return chain.invoke(result.json())
    

    def embed(self, text):
        return self.openai.embeddings.create(
            model="text-embedding-3-large",
            input=text
        )
