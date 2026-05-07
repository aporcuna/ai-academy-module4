import os
from langchain_core.documents import Document

def load_chunks_from_directory(chunks_dir: str) -> list[Document]:
    """
    Scans the chunks directory, parses the custom metadata headers,
    and returns a list of LangChain Document objects.
    """
    documents = []
    chunk_files = [f for f in os.listdir(chunks_dir) if f.endswith(".txt")]
    
    print(f"--- Parsing {len(chunk_files)} chunk files from disk ---")

    for file_name in chunk_files:
        file_path = os.path.join(chunks_dir, file_name)
        
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        # Extracting the metadata we injected in the chunking phase
        # Line 0: METADATA_SOURCE: ...
        # Line 1: METADATA_CHUNK_ID: ...
        # Line 2: --------------------
        source_file = lines[0].replace("METADATA_SOURCE: ", "").strip()
        chunk_id = lines[1].replace("METADATA_CHUNK_ID: ", "").strip()
        
        # Join the remaining lines as the actual page content
        content = "".join(lines[3:])
        
        # Construct the Document object
        doc = Document(
            page_content=content,
            metadata={
                "source": source_file,
                "chunk_id": chunk_id,
                "chunk_file": file_name
            }
        )
        documents.append(doc)
        
    return documents