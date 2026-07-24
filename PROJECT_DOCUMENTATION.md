# Smart PDF & Research Paper Q&A System using RAG
### B.Tech Final Year Internship Project Documentation

---

## 1. Project Overview

This project is a **Retrieval Augmented Generation (RAG)** based application that allows a user to upload a PDF research paper and ask natural-language questions about its content. Instead of reading the entire paper manually, the system retrieves the most relevant portions of the document and uses **Google Gemini** to generate an accurate, context-based answer.

**Tech Stack:**
| Component | Technology |
|---|---|
| Programming Language | Python |
| Framework (UI) | Streamlit |
| Orchestration | LangChain |
| Vector Database | FAISS |
| LLM & Embeddings | Google Gemini API |
| PDF Parsing | PyPDF2 |

---

## 2. Folder Structure

```
smart-pdf-qa/
│
├── app.py                   # Main Streamlit application (all modules)
├── requirements.txt         # Python dependencies
├── .env.example              # Sample environment file (rename to .env)
├── faiss_index/              # Auto-created folder that stores the vector DB
│   ├── index.faiss
│   └── index.pkl
└── PROJECT_DOCUMENTATION.md  # This file (report + PPT content)
```

---

## 3. System Architecture

```
                ┌───────────────────────┐
                │      User (Browser)    │
                │   Streamlit Web UI     │
                └───────────┬────────────┘
                            │  1. Upload PDF
                            ▼
                ┌───────────────────────┐
                │   PDF Upload Module    │
                │   (PyPDF2 extracts     │
                │    raw text)           │
                └───────────┬────────────┘
                            │  2. Raw text
                            ▼
                ┌───────────────────────┐
                │  Text Processing       │
                │  Module (LangChain     │
                │  RecursiveTextSplitter)│
                └───────────┬────────────┘
                            │  3. Text chunks
                            ▼
                ┌───────────────────────┐
                │  Embedding Module      │
                │  (Google Generative AI │
                │   Embeddings)          │
                └───────────┬────────────┘
                            │  4. Vector embeddings
                            ▼
                ┌───────────────────────┐
                │  FAISS Vector Database │
                │  (stored locally)      │
                └───────────┬────────────┘
                            │  5. User question
                            ▼
                ┌───────────────────────┐
                │  Similarity Search     │
                │  (Top-k relevant       │
                │   chunks retrieved)    │
                └───────────┬────────────┘
                            │  6. Context + Question
                            ▼
                ┌───────────────────────┐
                │  Google Gemini LLM     │
                │  (Generates answer)    │
                └───────────┬────────────┘
                            │  7. Final answer
                            ▼
                ┌───────────────────────┐
                │   Streamlit UI Output  │
                └───────────────────────┘
```

---

## 4. Flowchart (Simplified for PPT)

```
   START
     │
     ▼
 Upload PDF File
     │
     ▼
 Extract Text (PyPDF2)
     │
     ▼
 Split Text into Chunks (LangChain)
     │
     ▼
 Generate Embeddings (Gemini Embeddings)
     │
     ▼
 Store Embeddings in FAISS DB
     │
     ▼
 User Enters a Question
     │
     ▼
 Search FAISS for Relevant Chunks
     │
     ▼
 Send Context + Question to Gemini LLM
     │
     ▼
 Display Generated Answer
     │
     ▼
   END
```

---

## 5. Module Description

### 5.1 PDF Upload Module
- Accepts a PDF file through the Streamlit file uploader.
- Uses `PyPDF2.PdfReader` to loop through every page and extract raw text.
- Handles PDFs with no extractable text using error handling.

### 5.2 Text Processing Module
- Uses LangChain's `RecursiveCharacterTextSplitter`.
- Splits the raw text into chunks of 1000 characters with a 200-character overlap so context is not lost between chunks.

### 5.3 Embedding Generation Module
- Uses `GoogleGenerativeAIEmbeddings` (model: `embedding-001`) to convert each text chunk into a numeric vector that represents its meaning.

### 5.4 Vector Database Module (FAISS)
- Stores all chunk embeddings using `FAISS.from_texts()`.
- Saves the database locally (`faiss_index/`) using `save_local()` so it can be reloaded later without reprocessing the PDF.

### 5.5 Question Answering Module
- Loads the saved FAISS database.
- Performs a similarity search to fetch the top 4 most relevant chunks for the user's question.
- Passes the retrieved chunks (context) and the question to Gemini using a custom LangChain prompt template.
- Gemini generates a final, human-readable answer grounded in the document content.

### 5.6 Streamlit User Interface
- Sidebar: PDF upload + "Process PDF" button.
- Main area: text input box for the question + "Get Answer" button.
- Displays the generated answer directly on the page.

---

## 6. Hardware Requirements

| Component | Minimum Requirement |
|---|---|
| Processor | Intel i3 / equivalent or higher |
| RAM | 4 GB (8 GB recommended) |
| Storage | 500 MB free space |
| Internet | Required (for Gemini API calls) |

## 7. Software Requirements

| Component | Requirement |
|---|---|
| Operating System | Windows / Linux / macOS |
| Python Version | 3.9 or above |
| IDE | VS Code / PyCharm (any) |
| Browser | Chrome / Edge / Firefox (for Streamlit UI) |
| API Key | Google Gemini API Key |

---

## 8. How to Run the Project

```bash
# 1. Create and activate a virtual environment (optional but recommended)
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux/Mac

# 2. Install dependencies
pip install -r requirements.txt

# 3. Add your Gemini API key
# Rename .env.example to .env and paste your API key inside

# 4. Run the Streamlit app
streamlit run app.py
```

---

## 9. Sample Output (for PPT / Report Screenshot Section)

**Step 1 — Upload PDF**
```
Sidebar: [Choose a PDF file]  ->  research_paper.pdf uploaded
[Process PDF] clicked
✅ "PDF processed successfully! You can now ask questions."
```

**Step 2 — Ask a Question**
```
Question: "What is the main objective of this research paper?"

Answer: "The main objective of this research paper is to propose a
lightweight deep learning model that improves image classification
accuracy while reducing computational cost, as described in the
Introduction and Methodology sections of the document."
```

**Step 3 — Follow-up Question**
```
Question: "What dataset was used in the experiments?"

Answer: "The authors used the CIFAR-10 dataset to evaluate the
performance of their proposed model, as mentioned in the
Experimental Setup section."
```

---

## 10. Explanation of Each Code Section (for Viva)

| Code Section | Purpose | Key Function |
|---|---|---|
| Step 1 | Loads the Gemini API key securely from `.env` | `load_dotenv()` |
| Step 2 | Extracts raw text from the uploaded PDF | `get_pdf_text()` |
| Step 3 | Breaks large text into manageable chunks | `get_text_chunks()` |
| Step 4 | Converts chunks to embeddings & stores/loads FAISS DB | `create_vector_store()`, `load_vector_store()` |
| Step 5 | Retrieves relevant chunks and queries Gemini for an answer | `get_qa_chain()`, `get_answer()` |
| Step 6 | Builds the Streamlit interface (upload, question box, output) | `main()` |
| Step 7 | Entry point that runs the Streamlit app | `if __name__ == "__main__":` |

**Why RAG instead of feeding the whole PDF to the LLM?**
- Research papers can be long; LLMs have a limited context window.
- RAG retrieves only the *relevant* sections, making answers faster, cheaper, and more accurate.
- It reduces hallucination since the model answers strictly from retrieved context.

---

## 11. Testing Section (Paste-Ready for PPT Slides)

**Test Case 1 — PDF Text Extraction**
```python
pdf_text = get_pdf_text(sample_pdf)
assert len(pdf_text) > 0
print("PDF text extraction successful, length:", len(pdf_text))
```

**Test Case 2 — Text Chunking**
```python
chunks = get_text_chunks(pdf_text)
print("Total chunks created:", len(chunks))
assert len(chunks) > 0
```

**Test Case 3 — Vector Store Creation**
```python
vector_store = create_vector_store(chunks)
print("FAISS vector store created:", vector_store is not None)
```

**Test Case 4 — Question Answering**
```python
question = "What is the conclusion of this paper?"
answer = get_answer(question)
print("Q:", question)
print("A:", answer)
```

**Sample Test Result Table (for PPT)**

| Test Case | Input | Expected Result | Status |
|---|---|---|---|
| PDF Upload | research_paper.pdf | Text extracted successfully | ✅ Pass |
| Text Chunking | Extracted text | Chunks of ~1000 characters created | ✅ Pass |
| Vector Store | Text chunks | FAISS index created & saved | ✅ Pass |
| Q&A - In-context Question | "What is the dataset used?" | Correct answer from paper | ✅ Pass |
| Q&A - Out-of-context Question | "What is the capital of France?" | "Answer is not available in the provided document." | ✅ Pass |

---

## 12. Future Enhancements (Optional Slide)
- Support multiple PDF uploads at once
- Add chat history / conversational memory
- Deploy on Streamlit Cloud / Render for public access
- Add support for scanned PDFs using OCR
