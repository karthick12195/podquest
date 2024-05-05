__import__('pysqlite3')
import sys
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
import warnings
import streamlit as st
from snowflake.cortex import Complete
from langchain.vectorstores.chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.prompts import ChatPromptTemplate

# Add the specific warning you want to suppress
warnings.filterwarnings("ignore", category=FutureWarning)

conn = st.connection("snowflake")
SP_SESSION = conn.session()

# Hugging Face embedding model
EMBEDDING_MODEL = HuggingFaceEmbeddings(model_name="snowflake/arctic-embed-l")

# Directory for storing Chroma data
CHROMA_PATH = "chroma"

# Template for prompting user
PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Here is the question: {question}
"""


def get_answer_from_prompt(query_text):
    # Prepare the database
    embedding_function = EMBEDDING_MODEL
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the database
    results = db.similarity_search_with_relevance_scores(query_text, k=5)
    if not results or results[0][1] < 0.5:
        print("Unable to find matching results.")
        return "Unable to find matching results."

    # Construct prompt for response generation
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    print(prompt)

    # Generate response using Snowflake Cortex
    response_text = Complete("snowflake-arctic", prompt)

    # Gather sources for the response
    sources = [doc.metadata.get("source", None) for doc, _score in results]
    formatted_response = f"{response_text}\n\nSources: {sources}"
    return formatted_response
