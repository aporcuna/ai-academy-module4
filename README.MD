# Local RAG Pipeline: PDF & Video Intelligence

This project is a modular Retrieval-Augmented Generation (RAG) system designed to run entirely on your local machine. It allows you to "talk" to your documentation and video training materials using Llama 3 via Ollama.

```
📁 Project Structure
├── main.py              # Central Orchestrator (with feature flags)
├── app.py               # Streamlit-based Chatbot Interface
├── requirements.txt     # Project dependencies
├── chroma_db/           # Local Vector Database (Persistence)
├── chunks/              # Semantic text fragments (.txt)
├── data/                # RAW INPUT (Place your PDFs and MP4s here)
├── processed_texts/     # Full-text extractions from Step 1
└── src/
    ├── data_extraction/ # Step 1: Parsing PDFs and transcribing Videos
    ├── data_chunking/   # Step 2: Semantic splitting & Metadata injection
    ├── data_storage/    # Step 3: Local Embedding & Vector Indexing
    └── data_generation/ # Step 4: Retrieval (MMR) & LLM Logic
```

# Installation & Setup
## 1. The Brain: Ollama
This project uses Ollama to serve the LLM locally.

Download: ollama.com

Model: Open your terminal and run the following to ensure you have the model

```ollama pull llama3```

## 2. The Body: Python Environment
We recommend using a virtual environment (venv) to keep things clean.

Create and activate environment

```python -m venv venv```
```source venv/bin/activate  # On Windows: venv\Scripts\activate```

# Install all dependencies from requirements.txt
```pip install -r requirements.txt```


#  How to Use the Pipeline
## 1. The Backend (main.py)
The main.py script is your command center. It coordinates the extraction, chunking, and storage. It includes Feature Flags so you don't have to repeat time-consuming tasks (like video transcription).

### Run the FULL pipeline:
```python main.py```

### Skip Extraction (Use existing text files):
```python main.py --skip-extraction```

### Re-index only (Skip extraction and chunking):
```python main.py --skip-extraction --skip-chunking```

## 2. The Frontend (app.py)
Once your database is populated (Step 3 finished), launch the interactive chat interface:
```streamlit run app.py```

# Core Features & Methodology
Multimodal Extraction: High-fidelity PDF parsing combined with OpenAI Whisper for local video-to-text transcription.

Semantic Chunking: Documents are split into 1000-character segments with 20% overlap to maintain context across fragments.

Vector Search (MMR): We use Maximum Marginal Relevance (MMR) to query ChromaDB. This ensures the 10 chunks sent to the LLM are both highly relevant and diverse, preventing the model from getting "stuck" on redundant introduction slides.

Metadata Citations: Every response from the chatbot tells you exactly which file (PDF name or Video title) it used to find the information.

Strict Grounding: The assistant is instructed to answer only based on the provided context, significantly reducing hallucinations.


# Dependencies Breakdown
The requirements.txt covers:

PyMuPDF & Whisper: For data extraction.

LangChain & LangChain-Core: For pipeline orchestration.

Sentence-Transformers: For local embeddings (all-MiniLM-L6-v2).

ChromaDB: For local vector storage.

Ollama Bridge: To communicate with the Llama 3 model.

Streamlit: For the web interface.