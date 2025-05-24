# app.py
import streamlit as st
from utils.pdf_reader import load_pdfs
from utils.retriever import build_index
from gemini_funny_bot import get_funny_response
from image_generator import generate_image
import os

st.title("😂 Funny StoryBot (Powered by Gemini!)")

user_input = st.text_input("Ask me anything about the stories")

if "index" not in st.session_state:
    # Get the absolute path to the backend directory
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    pdf_paths = [
        os.path.join(backend_dir, "Alice_In_Wonderland.pdf"),
        os.path.join(backend_dir, "Gullivers_Travels.pdf"),
        os.path.join(backend_dir, "The_Arabian_Nights.pdf")
    ]
    docs = load_pdfs(pdf_paths)
    index, texts = build_index(docs)
    st.session_state.index = index
    st.session_state.texts = texts

if st.button("Get Funny Answer"):
    index = st.session_state.index
    texts = st.session_state.texts
    # Search similar content
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer("all-MiniLM-L6-v2")
    query_emb = model.encode([user_input])
    import numpy as np
    D, I = index.search(np.array(query_emb), k=1)
    
    if D[0][0] > 1.0:
        response = "I don't know, but I love cheese sandwiches! 🥪"
        st.write(response)
    else:
        text = texts[I[0][0]]
        funny_reply = get_funny_response(text)
        st.write(funny_reply)
        
        # Generate and display image
        with st.spinner('Generating image...'):
            img_path = generate_image(funny_reply[:100])
            if os.path.exists(img_path):
                try:
                    st.image(img_path, caption="Generated Image")
                except Exception as e:
                    st.error(f"Error displaying image: {str(e)}")
                    st.info("Showing default image instead")
                    default_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "default_image.png")
                    if os.path.exists(default_path):
                        st.image(default_path)
            else:
                st.error("Failed to generate image. Please try again.")
