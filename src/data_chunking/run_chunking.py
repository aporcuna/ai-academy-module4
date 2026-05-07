import os
from langchain_text_splitters import RecursiveCharacterTextSplitter
from data_extraction.utils.io_handler import ensure_directory

def run_chunking_pipeline(input_dir, output_dir):
    """
    Reads processed .txt files, splits them into semantic chunks,
    and saves each chunk as an individual file in the output_dir.
    """
    print(f"\n--- Starting Chunking Module ---")
    ensure_directory(output_dir)

    # 1. Setup the Splitter
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=512,
        chunk_overlap=100,
        length_function=len
    )

    # 2. Process each file in processed_texts
    files = [f for f in os.listdir(input_dir) if f.endswith(".txt")]
    
    total_chunks_created = 0

    for file_name in files:
        file_path = os.path.join(input_dir, file_name)
        
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Split the text
        chunks = text_splitter.split_text(content)
        
        # 3. Save each chunk to the /chunks folder
        base_name = file_name.replace(".txt", "")
        
        for i, chunk_text in enumerate(chunks):
            chunk_filename = f"{base_name}_chunk_{i:03d}.txt"
            chunk_path = os.path.join(output_dir, chunk_filename)
            
            with open(chunk_path, "w", encoding="utf-8") as chunk_file:
                # We prepend the metadata so the Embed module knows where it came from
                chunk_file.write(f"METADATA_SOURCE: {file_name}\n")
                chunk_file.write(f"METADATA_CHUNK_ID: {i}\n")
                chunk_file.write("-" * 20 + "\n")
                chunk_file.write(chunk_text)
            
            total_chunks_created += 1

    print(f"✅ Chunking Complete. Created {total_chunks_created} individual chunks in: {output_dir}")