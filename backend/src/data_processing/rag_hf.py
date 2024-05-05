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

# Set token
HUGGINGFACE_TOKEN = os.getenv("HUGGING_FACE_TOKEN")

# Instantiate HuggingFace as an LLM
llm = HuggingFaceEndpoint(
repo_id="HuggingFaceH4/zephyr-7b-beta",
task="text-generation",
max_new_tokens=512,
top_k=30,
temperature=0.1,
repetition_penalty=1.03,
huggingfacehub_api_token=HUGGINGFACE_TOKEN,
)

qa_retriever = vector_search.as_retriever()

# Define a basic question-answering prompt template
prompt_template = """

Use the following pieces of context to answer the question at the end.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

{context}

Question: {question}
"""
PROMPT = PromptTemplate(
    template=prompt_template, input_variables=["context", "question"]
)

# Create the question-answering model
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=qa_retriever,
    return_source_documents=True,
    chain_type="stuff",
    chain_type_kwargs={"prompt": PROMPT},
)

# Prompt the LLM
query = "How can I secure my MongoDB Atlas cluster?"
docs = qa_chain({"query": query})

print(docs["result"])
print("\nSource documents: ")
pprint.pprint(docs["source_documents"])