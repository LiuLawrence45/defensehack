from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from langchain_mongodb import MongoDBAtlasVectorSearch
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain_community.llms import HuggingFaceEndpoint
import pprint
import os
from dotenv import load_dotenv
load_dotenv()

uri = os.getenv("MONGO_URL")

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Initialize embeddings
HUGGINGFACE_TOKEN = os.getenv("HUGGING_FACE_TOKEN")
embeddings = HuggingFaceEmbeddings(model_name="thenlper/gte-large")

db = client["telegram"]
collection = db["data"]

# Retrieve documents from MongoDB collection
docs = list(collection.find({}))

# Create the MongoDB Atlas Vector Search instance
vector_search = MongoDBAtlasVectorSearch.from_connection_string(
    connection_string = uri,
    namespace = "telegram.data",
    embedding = embeddings,
    index_name="vector_index_test",
)

# Run the documents through the embeddings and add to the vectorstore
vector_search.add_documents(docs)