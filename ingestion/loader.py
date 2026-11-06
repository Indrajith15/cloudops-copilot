from langchain_community.document_loaders import TextLoader

def load_documents():
    file_path = "data/documents/gcp_cloud_run.txt"

    loader = TextLoader(file_path, encoding= "utf-8")

    documents = loader.load()

    return documents


if __name__ =="__main__":
    docs = load_documents()
    
    print("Number of documents:", len(docs))

    print("\nDocument content:\n")
    print(docs[0].page_content)

    print("\nMetadata:")
    print(docs[0].metadata)
