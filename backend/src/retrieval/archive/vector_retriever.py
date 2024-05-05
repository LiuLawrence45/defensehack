from pymongo import MongoClient
from langchain_openai import OpenAIEmbeddings
from langchain_openai import OpenAI
#from langchain.embeddings.openai import OpenAIEmbeddings
from langchain_mongodb import MongoDBAtlasVectorSearch
#from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from langchain_community.document_loaders import DirectoryLoader
#from langchain_community.llms import OpenAI
#from langchain.vectorstores import MongoDBAtlasVectorSearch
#from langchain.document_loaders import DirectoryLoader
#from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
import gradio as gr
from gradio.themes.base import Base
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

# Returns the corresponding vectorStore for chunked excerpts
def createVectorStore(client):
    
   dbName = "telegram"
   collectionName = "data"
   index_name = "vector_index"

   collection = client[dbName][collectionName]

   vector_search = MongoDBAtlasVectorSearch.from_connection_string(
      uri,
      dbName + "." + collectionName,
      OpenAIEmbeddings(disallowed_special=()),
      index_name=index_name
   )

   # vector_search._text_key = "chunk" # (included this before when the text was in the "chunk" key)

   return vector_search


def find_source_docs(docs, client):
    
    """
    Finds the source docs given a list of documents.
    """
    
    retrieved_docs = {
        source: [] for source in sources
    }
    for doc in docs:
        print("Doc metadata: ", doc.metadata["metadata"])
        source_name = doc.metadata["metadata"]["source_name"] # The formatting of the resultant doc as our metadata as a subfield of the default metadata
        source_id = doc.metadata["metadata"]["source_id"]
        collection = client["data"][source_name]
        retrieved_doc = collection.find_one({"_id": source_id})
        if retrieved_doc:
            
            already_exists = any(existing_doc['_id'] == retrieved_doc['_id'] for existing_doc in retrieved_docs[source_name])

            if not already_exists:
               retrieved_docs[source_name].append(retrieved_doc)
               print("Retrieved document with name: ", source_name)
    return retrieved_docs


def job(query, vector_search, client) -> Tuple[str, List[str]]:
   
   """
   Executable Job. Returns a tuple containing the following.

   (answer, docs).

   Docs has the following format

   {
      'new': [doc1, doc2, doc3, doc4, etc...],
      'reddit': [doc1, doc2, doc3, doc4, etc...],
      'youtube': [doc1, doc2, doc3, doc4, etc...],
   }
   """

   # Modifying query, and retrieving documents with it
   query_chain = QUERY_PROMPT | ChatOpenAI() | StrOutputParser()
   modified_query = query_chain.invoke({"query": query})

   # Retrieving additional docs (from all ragged)
   docs = vector_search.similarity_search(query=modified_query, k=25)
   retrieved_docs = find_source_docs(docs, client)

   # Defining main chain
   chain = RESPONSE_PROMPT | ChatOpenAI() | StrOutputParser()

   # Generating an answer with the original query
   answer = chain.invoke({
   "context": "\n".join(doc.page_content for doc in docs),
   "query": query

   })

   return answer, retrieved_docs


# Take sthe output provided by job, and returns a JSON serializable form of it
def process_as_json(data: Tuple[str, List[dict]]) -> str:
   # Convert ObjectId to str for JSON serialization
   def convert_id(obj):
      if isinstance(obj, bson.ObjectId):
         return str(obj)
      raise TypeError("Object of type ObjectId is not JSON serializable")

   # Assuming data[1] is a list of documents containing ObjectId instances
   # data[1] has the format {news: [doc1, doc2, ], youtube: [doc1, doc2, ], reddit: [doc1, doc2]}. fix as needed
   for source in sources:
      current_source = data[1][source]
      for doc in current_source:
         doc['_id'] = convert_id(doc['_id'])

   return json.dumps({"answer": data[0], "documents": data[1]}, default=convert_id)

if __name__ == '__main__':
   query = input("What's your query? ")
   answer, docs = job(query, createVectorStore(client), client)
   print(answer)
   