import streamlit as st
import scripts.query_data as query_data

conn = st.connection("snowflake")
SP_SESSION = conn.session()

def main():
    st.title("PodQuest: Use LLM to ask questions about science based tools from Huberman Lab podcast")
    # Input field for user question
    user_question = st.text_input("Ask a question")

    # Button to trigger query
    if st.button("Get Answer"):
        if user_question:
            # Call query_data.py function with user question as argument
            answer, context_text = query_data.get_answer_from_prompt(user_question, SP_SESSION)
            
            # Display answer
            st.write("Answer:", answer)

            if answer != "Unable to find answers from Huberman Lab":
                with st.expander("Show Relevant text from Podcast transcripts"):
                    st.markdown(context_text)
        else:
            st.warning("Please enter a question")

if __name__ == "__main__":
    main()
