# src/app.py
import streamlit as st
import os
import sys

# Setup paths for modular imports
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(BASE_DIR)
sys.path.append(os.path.join(BASE_DIR, "src"))

from data_generation.rag_engine import get_rag_response

# Page Config
st.set_page_config(page_title="Personal RAG Assistant", page_icon="🤖")
st.title("📚 Local RAG Chatbot")
st.markdown("Querying your PDFs and Videos via **Llama 3**")

# Database Path
DB_DIR = os.path.join(BASE_DIR, "chroma_db")

# Chat History initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Ask something about your data..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate Response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response, sources = get_rag_response(prompt, DB_DIR)
                
                # Format sources for the UI
                unique_sources = list(set(sources))
                source_text = "\n\n**Sources:** " + ", ".join(unique_sources)
                
                full_response = response + source_text
                st.markdown(full_response)
                
                # Add to history
                st.session_state.messages.append({"role": "assistant", "content": full_response})
            except Exception as e:
                st.error(f"Error: {str(e)}")
                st.info("Check if Ollama is running and Llama 3 is downloaded.")