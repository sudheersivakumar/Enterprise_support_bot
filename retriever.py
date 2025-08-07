
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
import os

def create_knowledge_base():
    """
    Loads all .txt files from knowledge_base/ and creates a FAISS vector store.
    """
    # Load documents
    loader = TextLoader("knowledge_base/password_reset.txt", encoding="utf-8")
    password_doc = loader.load()

    loader = TextLoader("knowledge_base/return_policy.txt", encoding="utf-8")
    return_doc = loader.load()

    # Combine documents
    docs = password_doc + return_doc

    # Split text
    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    split_docs = text_splitter.split_documents(docs)

    # Create embeddings
    embeddings = HuggingFaceEmbeddings()

    # Create FAISS vector store
    vectorstore = FAISS.from_documents(split_docs, embeddings)

    # Save to disk (optional)
    vectorstore.save_local("faiss_index")

    return vectorstore.as_retriever()
