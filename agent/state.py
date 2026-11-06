from typing import TypedDict, List
from langchain_core.documents import Document


class GraphState(TypedDict, total=False):

    question: str
    search_query: str
    documents: List[Document]
    relevant: bool
    retry_count: int
    max_retries: int
    answer: str
    faithfulness: bool