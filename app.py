
import os
import streamlit as st

# Load deployment secrets before importing backend modules
try:
    if "GOOGLE_API_KEY" in st.secrets:
        os.environ["GOOGLE_API_KEY"] = st.secrets["GOOGLE_API_KEY"]
except Exception:
    pass

from retrieval.vector_store import initialize_vector_store
from chains.rag_chain import get_agentic_answer


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="CloudOps Copilot",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# CUSTOM STYLING
# --------------------------------------------------

st.markdown("""
<style>
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1100px;
    }

    [data-testid="stSidebar"] {
        border-right: 1px solid rgba(128,128,128,0.2);
    }

    .stChatMessage {
        border-radius: 12px;
    }

    div[data-testid="stStatusWidget"] {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.title("☁️ CloudOps")

    st.caption("AI Cloud Troubleshooting Assistant")

    st.divider()

    st.subheader("About")

    st.write(
        "CloudOps Copilot uses Agentic RAG and LangGraph "
        "to troubleshoot cloud infrastructure issues "
        "using technical documentation."
    )

    st.divider()

    st.subheader("Capabilities")

    st.markdown("""
    - 🔎 Semantic document retrieval
    - 🧠 Agentic reasoning
    - 🔄 Query rewriting
    - 📚 Source document tracking
    - ✅ Faithfulness evaluation
    """)

    st.divider()

    st.subheader("Technology")

    st.markdown("""
    - Python
    - LangChain
    - LangGraph
    - Gemini
    - ChromaDB
    - Streamlit
    """)

    st.divider()

    if st.button(
        "🗑️ Clear conversation",
        use_container_width=True
    ):
        st.session_state.messages = []
        st.rerun()


# --------------------------------------------------
# APPLICATION HEADER
# --------------------------------------------------

st.title("☁️ CloudOps Copilot")

st.markdown(
    "Your intelligent assistant for diagnosing "
    "and troubleshooting cloud infrastructure."
)

st.caption(
    "Powered by Gemini · LangChain · LangGraph · ChromaDB"
)

st.divider()


# --------------------------------------------------
# CHAT HISTORY
# --------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []


# Display previous conversations

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if message["role"] == "assistant":

            faithfulness = message.get(
                "faithfulness", False
            )

            if faithfulness:
                st.success(
                    "✓ Automated faithfulness check passed"
                )
            else:
                st.warning(
                    "⚠ Automated faithfulness check did not pass"
                )

            # Display sources

            sources = message.get("sources", [])

            if sources:

                with st.expander("📚 View retrieved sources"):

                    for i, source in enumerate(sources):

                        st.markdown(
                            f"**Retrieved chunk {i + 1}**"
                        )

                        st.caption(
                            f"Source: {source['source']}"
                        )

                        st.write(source["content"])

                        st.divider()


# --------------------------------------------------
# USER INPUT
# --------------------------------------------------

question = st.chat_input(
    "Ask a cloud troubleshooting question..."
)


# --------------------------------------------------
# PROCESS USER QUESTION
# --------------------------------------------------

if question:

    # Save user message

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)


    # Generate assistant response

    with st.chat_message("assistant"):

        with st.spinner(
            "Investigating your cloud issue..."
        ):

            try:

                result = get_agentic_answer(question)

                answer = result["answer"]

                sources = [
                    {
                        "source": doc.metadata.get(
                            "source", "Unknown"
                        ),
                        "content": doc.page_content
                    }
                    for doc in result.get("sources", [])
                ]

                faithfulness = result.get(
                    "faithfulness", False
                )


                # Display answer

                st.markdown(answer)


                # Display faithfulness

                if faithfulness:

                    st.success(
                        "✓ Automated faithfulness check passed"
                    )

                else:

                    st.warning(
                        "⚠ Automated faithfulness check did not pass"
                    )


                # Display sources

                if sources:

                    with st.expander(
                        "📚 View retrieved sources"
                    ):

                        for i, source in enumerate(sources):

                            st.markdown(
                                f"**Retrieved chunk {i + 1}**"
                            )

                            st.caption(
                                f"Source: {source['source']}"
                            )

                            st.write(source["content"])

                            st.divider()


                # Save assistant message

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer,
                    "sources": sources,
                    "faithfulness": faithfulness
                })


            except Exception:

                error_message = (
                    "Sorry, something went wrong while "
                    "processing your request. "
                    "Please try again."
                )

                st.error(error_message)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": error_message,
                    "sources": [],
                    "faithfulness": False
                })
