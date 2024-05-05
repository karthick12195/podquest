import streamlit as st
import scripts.query_data as query_data
from langchain.vectorstores.chroma import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

def main():
    st.title("Question Answering App")
    EMBEDDING_MODEL = HuggingFaceEmbeddings(model_name="snowflake/arctic-embed-m")
    db = Chroma(persist_directory='chroma', embedding_function=EMBEDDING_MODEL)


    # Input field for user question
    user_question = st.text_input("Ask a question")

    # Button to trigger query
    if st.button("Get Answer"):
        if user_question:
            # Call query_data.py function with user question as argument
            answer = query_data.get_answer_from_prompt(user_question)
            
            # Display answer
            st.write("Answer:", answer)
        else:
            st.warning("Please enter a question")

if __name__ == "__main__":
    main()
