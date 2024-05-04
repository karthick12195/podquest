import warnings
from snowflake.ml.utils import connection_params
from snowflake.snowpark import Session
from snowflake.cortex import Complete
from langchain.vectorstores.chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.prompts import ChatPromptTemplate

# Add the specific warning you want to suppress
warnings.filterwarnings("ignore", category=FutureWarning)

# Snowflake connection parameters
SNOWFLAKE_LOGIN_OPTIONS = connection_params.SnowflakeLoginOptions("xvb49931")

# Snowflake session creation
SP_SESSION = Session.builder.configs(SNOWFLAKE_LOGIN_OPTIONS).create()

# Hugging Face embedding model
EMBEDDING_MODEL = HuggingFaceEmbeddings(model_name="snowflake/arctic-embed-l")

# Directory for storing Chroma data
CHROMA_PATH = "chroma"

# Template for prompting user
PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""


def get_answer_from_prompt(query_text):
    # Prepare the database
    embedding_function = EMBEDDING_MODEL
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the database
    results = db.similarity_search_with_relevance_scores(query_text, k=5)
    if not results or results[0][1] < 0.2:
        print("Unable to find matching results.")
        return

    # Construct prompt for response generation
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    # print(prompt)

    # Generate response using Snowflake Cortex
    response_text = Complete("snowflake-arctic", prompt)

    # Gather sources for the response
    sources = [doc.metadata.get("source", None) for doc, _score in results]
    formatted_response = f"{response_text}\n\nSources: {sources}"
    return formatted_response
