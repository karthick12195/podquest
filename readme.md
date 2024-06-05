# PodQuest
PodQuest is a project aimed at creating a chatbot that answers questions on science-related tools for everyday life, drawing from episodes of the Huberman Lab podcast. The chatbot utilizes advanced techniques such as Retrieval-Augmented Generation (RAG) to generate informative responses based on the content of the podcast transcripts.

## Overview
The project contains scripts to facilitate the extraction, processing, and querying of data from the Huberman Lab podcast transcripts. These scripts are designed to automate the process of downloading transcripts from YouTube, creating embeddings for efficient retrieval, and responding to user queries with relevant information.

## Project Structure
- **scripts/**
    - **download_transcripts.py**: This script utilizes the YouTubeTranscriptApi and Pytubefix to download transcripts from the Huberman Lab YouTube channel. Transcripts are saved locally in the transcripts/ folder (not included in the Git repository).
    - **rag_engine.py**: This script processes the transcripts stored in the transcripts/ folder to create a vector database. The embeddings are based on the Snowflake Arctic model available in Huggingface. It utilizes Langchain for various tasks related to natural language processing.
    - **query_data.py**: This script takes a question as an argument and uses the embeddings generated in the previous step to retrieve the top relevant chunks from the transcripts. It then calls the Snowflake Cortex LLM (Large Language Model) to generate answers based on the retrieved chunks.

## Usage
To run the PodQuest project, follow these steps:

- Clone the repository to your local machine.
- Set up a conda environment using the provided requirements.txt file:
- ```conda create --name podquest --file requirements.txt```
- Execute the scripts in the scripts/ folder in the following order:
    - Run `download_transcripts.py` to download transcripts from the Huberman Lab YouTube channel.
    - Run `rag_engine.py` to process the transcripts and create the vector database.
    - Utilize `query_data.py` to ask questions and receive answers based on the processed transcripts.

## Snowflake Setup
Instructions for setting up Snowflake for use with this project will be added in a future update.

## Contributing
Contributions to PodQuest are welcome! If you have ideas for improvements or new features, feel free to open an issue or submit a pull request.

## License
This project is licensed under the MIT License.

## Acknowledgements
- The Huberman Lab podcast for providing valuable content for this project.
- Huggingface for their Snowflake Arctic model and other NLP tools.
- Langchain for assisting with natural language processing tasks.
- Snowflake for providing the Cortex LLM for answering user queries.
