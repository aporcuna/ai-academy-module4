import fitz 
import os

def extract_text_from_pdf(pdf_path: str) -> str:
    try:
        doc = fitz.open(pdf_path)
        text = f"SOURCE_FILE: {os.path.basename(pdf_path)}\n\n"
        for page in doc:
            text += page.get_text() + "\n"
        doc.close()
        return text
    except Exception as e:
        return f"ERROR processing {pdf_path}: {e}"