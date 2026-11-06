from langgraph.graph import StateGraph, START, END
from agent.nodes import check_faithfulness

from agent.state import GraphState

from agent.nodes import (
    retrieve,
    grade_documents,
    rewrite_query,
    generate_answer,
    fallback
)


# Decide what happens after document grading
def decide_after_grading(state):

    if state.get("relevant", False):
        return "generate"

    if state.get("retry_count", 0) < state.get("max_retries", 2):
        return "rewrite"

    return "fallback"


# Build the graph
workflow = StateGraph(GraphState)


# Register nodes
workflow.add_node("retrieve", retrieve)
workflow.add_node("grade", grade_documents)
workflow.add_node("rewrite", rewrite_query)
workflow.add_node("generate", generate_answer)
workflow.add_node("fallback", fallback)
workflow.add_node("faithfulness", check_faithfulness)


# Connect nodes
workflow.add_edge(START, "retrieve")
workflow.add_edge("retrieve", "grade")


# Conditional routing
workflow.add_conditional_edges(
    "grade",
    decide_after_grading,
    {
        "generate": "generate",
        "rewrite": "rewrite",
        "fallback": "fallback"
    }
)


# Retry goes back to retrieval
workflow.add_edge("rewrite", "retrieve")


# Finish workflow
workflow.add_edge("generate", "faithfulness")
workflow.add_edge("faithfulness", END)


# Compile graph
app = workflow.compile()