from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

def get_relevant_context(query: str, db_dir: str, k: int = 10):
    """
    Connects to ChromaDB and retrieves the most relevant chunks.
    Returns a tuple of (context_string, list_of_source_documents).
    """
    # 1. Initialize the same embedding model used during storage
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # 2. Connect to the existing Vector DB
    vector_db = Chroma(
        persist_directory=db_dir,
        embedding_function=embeddings
    )

    # 3. Perform Similarity Search
    # retrieved_docs = vector_db.similarity_search(query, k=k)
    retrieved_docs = vector_db.as_retriever(
        search_type="mmr", 
        search_kwargs={'k': k, 'fetch_k': 20}
    ).invoke(query)
    
    # 4. Prepare the context string for the LLM
    context_text = "\n\n---\n\n".join([doc.page_content for doc in retrieved_docs])
    
    return context_text, retrieved_docs