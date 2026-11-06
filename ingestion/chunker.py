from langchain_text_splitters import RecursiveCharacterTextSplitter
from ingestion.loader import load_documents

def split_documents():
    documents = load_documents()

    text_splitters = RecursiveCharacterTextSplitter(
        chunk_size = 300,
        chunk_overlap = 50
    )

    chunks = text_splitters.split_documents(documents)

    return chunks

if __name__ == "__main__":
    chunks = split_documents()
    print("Number of chunks:", len(chunks))
    for i, chunk in enumerate(chunks):
        print(f"\n -- Chunk {i+1} -- ")
        print(chunk.metadata)