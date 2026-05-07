# data_extraction/run_extraction.py
import os
from .utils.io_handler import ensure_directory, save_text
from .processors.pdf_processor import extract_text_from_pdf
from .processors.video_processor import load_whisper_model, transcribe_video

def run_extraction_pipeline(input_dir, output_dir):
    ensure_directory(input_dir)
    ensure_directory(output_dir)
    
    files = os.listdir(input_dir)
    pdfs = [f for f in files if f.lower().endswith('.pdf')]
    videos = [f for f in files if f.lower().endswith(('.mp4'))]

    print(f"--- Starting Extraction Module ---")

    for name in pdfs:
        print(f"Processing PDF: {name}")
        text = extract_text_from_pdf(os.path.join(input_dir, name))
        save_text(name, text, output_dir)

    if videos:
        model = load_whisper_model("base")
        for name in videos:
            print(f"Processing Video: {name}")
            transcript = transcribe_video(os.path.join(input_dir, name), model)
            save_text(name, transcript, output_dir)
            
    print(f"--- Extraction Module Finished ---")