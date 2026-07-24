"""
Project: Smart PDF & Research Paper Q&A System using RAG
Description: This app lets a user upload a PDF research paper and ask
             questions about it. It uses LangChain + FAISS + Google Gemini
             to build a simple Retrieval Augmented Generation (RAG) system.

Tech Stack: Python, Streamlit, LangChain, FAISS, Google Gemini API, PyPDF2
Author: (Your Name) - Final Year B.Tech CSE Internship Project
"""

# ---------------------------------------------------------
# STEP 0: Import required libraries
# ---------------------------------------------------------
import os
import streamlit as st
from dotenv import load_dotenv

from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import FAISS

# ---------------------------------------------------------
# STEP 1: Load API key from .env file
# ---------------------------------------------------------
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# Folder where the FAISS vector database will be saved locally
FAISS_DB_PATH = "faiss_index"


# ---------------------------------------------------------
# STEP 2: PDF Upload Module - Extract text from PDF pages
# ---------------------------------------------------------
def get_pdf_text(pdf_file):
    """Reads a PDF file and extracts text from every page."""
    text = ""
    try:
        pdf_reader = PdfReader(pdf_file)
        for page in pdf_reader.pages:
            page_text = page.extract_text()
            if page_text:  # only add if text was found on that page
                text += page_text
    except Exception as e:
        st.error(f"Error while reading PDF: {e}")
    return text


# ---------------------------------------------------------
# STEP 3: Text Processing Module - Split text into chunks
# ---------------------------------------------------------
def get_text_chunks(raw_text):
    """Splits the extracted text into smaller overlapping chunks."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,       # each chunk has ~1000 characters
        chunk_overlap=200      # 200 characters overlap to keep context
    )
    chunks = splitter.split_text(raw_text)
    return chunks

# STEP 4: Embedding + Vector Database Module (FAISS)
# ---------------------------------------------------------
def create_vector_store(text_chunks):
    """Converts text chunks into embeddings and stores them in FAISS."""
    try:
        embeddings = GoogleGenerativeAIEmbeddings(
            model="gemini-embedding-001",
            google_api_key=GOOGLE_API_KEY
        )
        vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)

        # Save the vector database locally so it can be reused
        vector_store.save_local(FAISS_DB_PATH)
        return vector_store
    except Exception as e:
        st.error(f"Error while creating vector store: {e}")
        return None


def load_vector_store():
    """Loads a previously saved FAISS vector database from disk."""
    embeddings = GoogleGenerativeAIEmbeddings(
        model="gemini-embedding-001",
        google_api_key=GOOGLE_API_KEY
    )
    vector_store = FAISS.load_local(
        FAISS_DB_PATH,
        embeddings,
        allow_dangerous_deserialization=True
    )
    return vector_store


# ---------------------------------------------------------
# STEP 5: Question Answering Module - Gemini + RAG
# ---------------------------------------------------------
def build_prompt(context, question):
    """Builds the final prompt that is sent to Gemini using retrieved context."""
    prompt = f"""
    Answer the question as detailed as possible using only the given context.
    If the answer is not available in the context, just say
    "Answer is not available in the provided document."
    Do not make up an answer.

    Context:
    {context}

    Question:
    {question}

    Answer:
    """
    return prompt


def get_answer(user_question):
    """Retrieves relevant chunks from FAISS and generates an answer using Gemini."""
    try:
        vector_store = load_vector_store()

        # Search FAISS for chunks most similar to the user question
        relevant_docs = vector_store.similarity_search(user_question, k=4)

        # Combine the retrieved chunks into a single context string
        context_text = "\n\n".join([doc.page_content for doc in relevant_docs])

        # Build the final prompt with context + question
        final_prompt = build_prompt(context_text, user_question)

        # Send the prompt directly to the Gemini chat model
        model = ChatGoogleGenerativeAI(
            model="gemini-3.5-flash-lite",
            temperature=0.3,
            google_api_key=GOOGLE_API_KEY
        )
        response = model.invoke(final_prompt)

        # Newer Gemini models can return content as a list of blocks
        # instead of a plain string, so we pull out just the text parts
        answer_content = response.content

        if isinstance(answer_content, list):
            text_parts = []
            for block in answer_content:
                if isinstance(block, dict) and block.get("type") == "text":
                    text_parts.append(block.get("text", ""))
                elif isinstance(block, str):
                    text_parts.append(block)
                elif hasattr(block, "text"):
                    text_parts.append(getattr(block, "text", ""))
            final_answer = "\n".join(text_parts).strip()
        else:
            final_answer = str(answer_content)

        return final_answer

    except Exception as e:
        return f"Error while generating answer: {e}"


# ---------------------------------------------------------
# STEP 6: Streamlit Chat User Interface
# ---------------------------------------------------------
def main():
    st.set_page_config(page_title="Smart PDF Q&A (RAG)", page_icon="📄")
    st.title("📄 Smart PDF & Research Paper Q&A System")
    st.write("Upload a research paper (PDF), then chat with it below.")

    # Session state keeps the chat history alive between reruns
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "pdf_ready" not in st.session_state:
        st.session_state.pdf_ready = os.path.exists(FAISS_DB_PATH)

    # Sidebar - PDF upload section
    with st.sidebar:
        st.header("Upload PDF")
        pdf_file = st.file_uploader("Choose a PDF file", type=["pdf"])

        if st.button("Process PDF"):
            if pdf_file is not None:
                with st.spinner("Reading and processing PDF..."):
                    raw_text = get_pdf_text(pdf_file)

                    if raw_text.strip() == "":
                        st.error("No readable text found in this PDF.")
                    else:
                        text_chunks = get_text_chunks(raw_text)
                        create_vector_store(text_chunks)
                        st.session_state.pdf_ready = True
                        st.session_state.chat_history = []  # reset chat for new PDF
                        st.success("PDF processed successfully! You can now ask questions.")
            else:
                st.warning("Please upload a PDF file first.")

    # Show past chat messages (chatbot-style bubbles)
    for role, message in st.session_state.chat_history:
        with st.chat_message(role):
            st.markdown(message)

    # Chat input box (stays pinned at the bottom, like a real chatbot)
    user_question = st.chat_input("Ask a question about the uploaded PDF...")

    if user_question:
        if not GOOGLE_API_KEY:
            st.error("Google API Key not found. Please set it in the .env file.")
        elif not st.session_state.pdf_ready:
            st.warning("Please upload and process a PDF first.")
        else:
            # Show the user's message immediately
            st.session_state.chat_history.append(("user", user_question))
            with st.chat_message("user"):
                st.markdown(user_question)

            # Generate and show the assistant's answer
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    answer = get_answer(user_question)
                    st.markdown(answer)
            st.session_state.chat_history.append(("assistant", answer))


# ---------------------------------------------------------
# STEP 7: Run the app
# ---------------------------------------------------------
if __name__ == "__main__":
    main()