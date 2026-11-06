import os
from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

load_dotenv()


def create_vector_store():

    # Initialize Google's query embedding model
    embedding_model = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001",
        google_api_key=os.getenv("GOOGLE_API_KEY"),
        task_type="RETRIEVAL_QUERY"
    )

    # Connect to our existing ChromaDB collection
    vector_store = Chroma(
        collection_name="cloudops_documents",
        embedding_function=embedding_model,
        persist_directory="./chroma_db"
    )

    return vector_store