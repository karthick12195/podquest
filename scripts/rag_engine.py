from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain.vectorstores.chroma import Chroma
import os
import shutil
import warnings
# Add the specific warning you want to suppress
warnings.filterwarnings("ignore", category=FutureWarning)

# Initialize Hugging Face model for embeddings
model = HuggingFaceEmbeddings(model_name="snowflake/arctic-embed-l")

# Constants for paths
CHROMA_PATH = "chroma"
DATA_PATH = "data/transcripts"

def main():
    """
    Main function to generate data store for the RAG engine.
    """
    generate_data_store()

def generate_data_store():
    """
    Generate data store for the RAG engine.
    """
    documents = load_documents()
    print(f"Loaded {len(documents)} documents.")

    chunks = split_text(documents)
    save_to_chroma(chunks)

def load_documents():
    """
    Load documents from the specified directory.
    
    Returns:
        list[Document]: List of loaded documents.
    """
    loader = DirectoryLoader(DATA_PATH, glob="*.md")
    documents = loader.load()
    return documents

def split_text(documents: list[Document]):
    """
    Split text into chunks.
    
    Args:
        documents (list[Document]): List of documents.
    
    Returns:
        list[Document]: List of chunks.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=500,
        length_function=len,
        add_start_index=True,
    )
    chunks = text_splitter.split_documents(documents)
    print(f"Split {len(documents)} documents into {len(chunks)} chunks.")

    # Example of accessing document content and metadata
    document = chunks[10]
    print(document.page_content)
    print(document.metadata)

    return chunks

def save_to_chroma(chunks: list[Document]):
    """
    Save chunks to Chroma database.
    
    Args:
        chunks (list[Document]): List of document chunks.
    """
    # Clear out the database first.
    if os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    # Create a new DB from the documents.
    db = Chroma.from_documents(
        chunks, model, persist_directory=CHROMA_PATH
    )

    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")

if __name__ == "__main__":
    main()
