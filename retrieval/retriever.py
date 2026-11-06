from retrieval.vector_store import create_vector_store


def get_retriever(k=3, filters = None):

    # Load the existing vector store
    vector_store = create_vector_store()

    search_kwargs = {"k": k}
    if filters:
        search_kwargs["filter"] = filters

    # Convert vector store into a retriever
    retriever = vector_store.as_retriever(
         search_kwargs=search_kwargs
    )

    return retriever


def search_similar_documents(question, k=3, filters=None):

    vector_store = create_vector_store()

    results = vector_store.similarity_search_with_score(
        query=question,
        k=k,
        filter=filters
    )

    return results



def evaluate_retrieval(question, k=5):

    results = search_similar_documents(
        question=question,
        k=k
    )

    evaluation = []

    for document, score in results:

        evaluation.append({
            "content": document.page_content,
            "source": document.metadata.get("source"),
            "distance": score
        })

    return evaluation