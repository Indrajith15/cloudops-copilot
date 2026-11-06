import os 
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from ingestion.chunker import split_documents
from dotenv import load_dotenv

load_dotenv()

def create_embeddings():
    chunks = split_documents()

    embedding_model = GoogleGenerativeAIEmbeddings(
        model = "gemini-embedding-001",
        google_api_key = os.getenv("GOOGLE_API_KEY"),
        task_type="RETRIEVAL_DOCUMENT"
    )

    vectors = embedding_model.embed_documents(
        [chunk.page_content for chunk in chunks]
    )
    return chunks, vectors

if __name__ == "__main__":

    chunks, vectors = create_embeddings()

    print("Number of chunks:", len(chunks))
    print("Number of embeddings:", len(vectors))
    print("Embedding dimensions:", len(vectors[0]))