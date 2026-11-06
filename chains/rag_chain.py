import os
from dotenv import load_dotenv
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

from retrieval.retriever import get_retriever
from chains.prompts import rag_prompt

load_dotenv()


# Initialize retriever
retriever = get_retriever(k=5)


# Initialize Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0
)


# Format retrieved documents into context
def format_docs(documents):
    return "\n\n".join(
        document.page_content for document in documents
    )


# Build LCEL RAG chain
rag_chain = (
    {
        "context": retriever | RunnableLambda(format_docs),
        "question": RunnablePassthrough()
    }
    | rag_prompt
    | llm
    | StrOutputParser()
)


def get_answer(question):

    # Retrieve documents separately for source tracking
    # Rewrite the user's question
    search_query = rewrite_query(question)

# Retrieve documents using the improved query
    source_documents = retriever.invoke(search_query)

    # Generate answer
    answer = rag_chain.invoke(question)

    return {
        "answer": answer,
        "sources": source_documents
    }




# Query rewriting prompt
rewrite_prompt = ChatPromptTemplate.from_template("""
You are a cloud troubleshooting search assistant.

Rewrite the user's question into a clear and specific
search query for retrieving relevant cloud documentation.

Preserve the original meaning.
Do not answer the question.
For every factual troubleshooting recommendation:
- Cite the supporting source using its [Source: filename] label.
- Do not cite sources that do not support the statement.
- If the context does not contain enough information, say so.
- Never invent source names or citations.

User question:
{question}

Improved search query:
""")


# Create query rewriting chain
rewrite_chain = rewrite_prompt | llm | StrOutputParser()


def rewrite_query(question):

    rewritten_question = rewrite_chain.invoke({
        "question": question
    })

    return rewritten_question.strip()



def get_agentic_answer(question):

    from agent.graph import app

    result = app.invoke({
        "question": question,
        "search_query": question,
        "documents": [],
        "relevant": False,
        "retry_count": 0,
        "max_retries": 2,
        "answer": ""
    })

    return {
    "answer": result["answer"],
    "sources": result.get("documents", []),
    "faithfulness": result.get("faithfulness", False)
}