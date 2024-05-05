import streamlit as st
import scripts.query_data as query_data

def main():
    st.title("PodQuest: Use LLM to ask questions about science based tools from Huberman Lab podcast")
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
