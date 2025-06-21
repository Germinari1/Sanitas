import os
from langchain_community.document_loaders import DirectoryLoader, TextLoader, PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain.chains.retrieval_qa.base import RetrievalQA
from langchain.agents import Tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain import hub
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

def build_file_retrieval_tool(
    docs_path: str,
    qa_model_env: str = "HOSPITAL_QA_MODEL",
    chunk_size: int = 1000,
    chunk_overlap: int = 200,
    k: int = 5,
    persist_directory: str = "vec_store_data/chroma_db"
) -> Tool:
    """
    Loads .txt/.pdf files under docs_path, builds a RetrievalQA chain,
    and wraps it as a LangChain Tool.
    """
    # load files for retrieval 
    # NOTE: currently .txt and .pdf files are supported
    txt_loader = DirectoryLoader(docs_path, glob="**/*.txt", loader_cls=TextLoader)
    pdf_loader = DirectoryLoader(docs_path, glob="**/*.pdf", loader_cls=PyPDFLoader)
    raw_docs = txt_loader.load() + pdf_loader.load()
    
    # docs -> chunks
    splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size,chunk_overlap=chunk_overlap,)
    docs = splitter.split_documents(raw_docs)
    
    # embedd/index
    embeddings = HuggingFaceEmbeddings(model_name=os.getenv('FILE_RETRIEVAL_EMBEDDINGS'))
    
    vectorstore = Chroma.from_documents(
        documents=docs, 
        embedding=embeddings, 
        persist_directory=persist_directory
    )
    
    retriever = vectorstore.as_retriever(search_kwargs={"k": k})
    
    llm = ChatGoogleGenerativeAI(model = os.getenv('FILE_RETRIEVAL_MODEL'))
    
    retrieval_qa_chat_prompt = hub.pull("langchain-ai/retrieval-qa-chat")

    stuff_chain = create_stuff_documents_chain(
        llm=llm,
        prompt=retrieval_qa_chat_prompt
    )

    rag_chain = create_retrieval_chain(
        retriever=retriever,
        combine_docs_chain=stuff_chain
    )
    
    return Tool(
        name="HospitalDocs",
        func=lambda question: rag_chain.invoke({"input": question})["answer"],
        description=(
            "Use for hospital-specific info (hours, specialties, general info) "
            "from the .txt/.pdf files. Pass your question; this will retrieve "
            "and answer from the right document chunks."
        ),
    )