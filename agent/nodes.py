import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

from retrieval.retriever import get_retriever
from chains.prompts import rag_prompt

load_dotenv()


# Initialize Gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    google_api_key=os.getenv("GOOGLE_API_KEY"),
    temperature=0
)


# Initialize retriever
retriever = get_retriever(k=5)


# 1. Retrieve documents
def retrieve(state):

    query = state.get("search_query") or state["question"]

    documents = retriever.invoke(query)

    return {"documents": documents}


# 2. Grade document relevance
grading_prompt = ChatPromptTemplate.from_template("""
You are evaluating retrieved cloud troubleshooting documents.

Question:
{question}

Retrieved documents:
{documents}

Are these documents relevant and useful for answering the question?

Respond with ONLY:
yes
or
no
""")

grading_chain = grading_prompt | llm | StrOutputParser()


def grade_documents(state):

    documents = state.get("documents", [])

    if not documents:
        return {"relevant": False}

    document_text = "\n\n".join(
        doc.page_content for doc in documents
    )

    result = grading_chain.invoke({
        "question": state["question"],
        "documents": document_text
    })

    return {"relevant": result.strip().lower().startswith("yes")}


# 3. Rewrite the search query
rewrite_prompt = ChatPromptTemplate.from_template("""
Rewrite the user's cloud troubleshooting question
into a clearer search query for retrieving technical documentation.

Do not answer the question.

Original search query:
{search_query}

Improved search query:
""")

rewrite_chain = rewrite_prompt | llm | StrOutputParser()


def rewrite_query(state):

    current_query = state.get("search_query") or state["question"]

    rewritten_query = rewrite_chain.invoke({
        "search_query": current_query
    })

    return {
        "search_query": rewritten_query.strip(),
        "retry_count": state.get("retry_count", 0) + 1
    }

# 4. Generate the final answer
answer_chain = rag_prompt | llm | StrOutputParser()
faithfulness_prompt = ChatPromptTemplate.from_template("""
You are evaluating a cloud troubleshooting answer.

Context:
{context}

Answer:
{answer}

Does the answer contain claims unsupported by the context?

Respond ONLY with:
PASS
or
FAIL
""")

faithfulness_chain = faithfulness_prompt | llm | StrOutputParser()

def check_faithfulness(state):

    documents = state.get("documents", [])

    context = "\n\n".join(
        doc.page_content for doc in documents
    )

    result = faithfulness_chain.invoke({
        "context": context,
        "answer": state["answer"]
    })

    return {
        "faithfulness": result.strip().upper().startswith("PASS")
    }


def generate_answer(state):

    documents = state.get("documents", [])

    context = "\n\n".join(
        f"[Source: {doc.metadata.get('source', 'Unknown')}]\n"
        f"{doc.page_content}"
        for doc in documents
    )

    answer = answer_chain.invoke({
        "context": context,
        "question": state["question"]
    })

    return {"answer": answer}


# 5. Fallback response
def fallback(state):

    return {
        "answer": (
            "I couldn't find sufficiently relevant information "
            "in the available troubleshooting documents. "
            "Please provide more details about the cloud service, "
            "error message, and recent changes."
        )
    }