from pymongo import MongoClient
from langchain_openai import OpenAIEmbeddings
from langchain_openai import OpenAI
#from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_community.document_loaders import DirectoryLoader
from langchain.chains import RetrievalQA
from langchain_core.tracers.context import tracing_v2_enabled
import dotenv
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

from langchain_core.runnables import RunnableParallel, RunnablePassthrough, RunnableLambda

from typing import Tuple, List
import json
import bson

dotenv.load_dotenv()





