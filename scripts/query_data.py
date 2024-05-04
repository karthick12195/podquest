import argparse
import os
from dataclasses import dataclass
from langchain.vectorstores.chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.prompts import ChatPromptTemplate
# import replicate

from snowflake.snowpark import Session
from snowflake.ml.utils import connection_params

params = connection_params.SnowflakeLoginOptions("xvb49931")
sp_session = Session.builder.configs(params).create()

from snowflake.cortex import Complete


EMBEDDING_MODEL = HuggingFaceEmbeddings(model_name="snowflake/arctic-embed-l")

# os.environ["REPLICATE_API_TOKEN"] = 'r8_0BdpSPQ6tS3kue3tO1g8cQo8dWYFCE71BfxJJ'

CHROMA_PATH = "chroma"

PROMPT_TEMPLATE = """
Answer the question based only on the following context:

{context}

---

Answer the question based on the above context: {question}
"""


def main():
    # Create CLI.
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text

    # Prepare the DB.
    embedding_function = EMBEDDING_MODEL
    db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)

    # Search the DB.
    results = db.similarity_search_with_relevance_scores(query_text, k=5)
    if len(results) == 0 or results[0][1] < 0.2:
        print(f"Unable to find matching results.")
        return

    context_text = "\n\n---\n\n".join([doc.page_content for doc, _score in results])
    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query_text)
    print(prompt)

    input = {
    "prompt": prompt,
    "temperature": 0.2
    }

    # output = replicate.run(
    # "snowflake/snowflake-arctic-instruct",
    # input=input
    # )

    response_text = Complete("snowflake-arctic", prompt)

    # model = ChatOpenAI()
    # response_text = model.predict(prompt)

    sources = [doc.metadata.get("source", None) for doc, _score in results]
    formatted_response = f"Response: {response_text}\nSources: {sources}"
    print(formatted_response)


if __name__ == "__main__":
    main()