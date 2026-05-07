from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from .document_loader import load_chunks_from_directory

def run_storage_pipeline(chunks_dir: str, db_dir: str):
    """
    Orchestrates the loading of documents, generation of embeddings,
    and storage in the vector database.
    """
    print("\n--- Starting Storage & Indexing Module ---")
    
    # 1. Load the prepared documents using our helper
    documents = load_chunks_from_directory(chunks_dir)
    
    if not documents:
        print("⚠️ No documents found to index. Skipping storage.")
        return

    # 2. Initialize Embeddings (Local Model)
    print("Initializing embedding model: all-MiniLM-L6-v2...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # 3. Create and Save to ChromaDB
    print(f"Indexing {len(documents)} vectors into: {db_dir}")
    
    # This command creates the DB if it doesn't exist or updates it
    vector_db = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        persist_directory=db_dir
    )
    
    print("✅ Storage phase complete. Database is ready.")