# 📄 Smart PDF & Research Paper Q&A System (RAG)

A simple **Retrieval Augmented Generation (RAG)** web app that lets you upload a PDF research paper and chat with it — ask questions and get answers grounded in the document's actual content.

🔗 **Live demo:** [pdfanalyzerinternsummer.streamlit.app](https://pdfanalyzerinternsummer.streamlit.app/)

> Built as a B.Tech CSE Summer Internship project.

---

## ✨ Features

- 📤 Upload any PDF research paper
- 🧠 Automatic text extraction, chunking, and embedding
- 🔍 Semantic search over the document using FAISS
- 💬 Chat-style interface — ask follow-up questions, see conversation history
- ⚡ Powered by Google Gemini for fast, accurate answers grounded in your PDF

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| UI | [Streamlit](https://streamlit.io) |
| Orchestration | [LangChain](https://www.langchain.com) |
| Vector Database | [FAISS](https://github.com/facebookresearch/faiss) |
| LLM & Embeddings | [Google Gemini API](https://ai.google.dev) |
| PDF Parsing | [PyPDF2](https://pypi.org/project/PyPDF2/) |

---

## 🧩 How It Works

```
Upload PDF → Extract Text → Split into Chunks → Generate Embeddings
    → Store in FAISS → User asks a question → Retrieve relevant chunks
    → Send context + question to Gemini → Display answer
```

See [`PROJECT_DOCUMENTATION.md`](./PROJECT_DOCUMENTATION.md) for the full architecture diagram, module breakdown, and testing notes.

---

## 🚀 Getting Started Locally

### 1. Clone the repo
```bash
git clone https://github.com/Ganeshkumar841/pdfQnA.git
cd pdfQnA
```

### 2. Create a virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # macOS/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Add your Gemini API key
Copy `.env.example` to `.env` and paste your key:
```
GOOGLE_API_KEY=your_google_gemini_api_key_here
```
Get a free key at [aistudio.google.com/app/apikey](https://aistudio.google.com/app/apikey).

### 5. Run the app
```bash
streamlit run app.py
```
The app opens at `http://localhost:8501`.

---

## ☁️ Deployment

This app is deployed on **Streamlit Community Cloud**. To deploy your own copy:

1. Push this repo to your own GitHub account.
2. Go to [share.streamlit.io](https://share.streamlit.io) and sign in with GitHub.
3. Click **Create app** → select your repo, branch `main`, and file `app.py`.
4. Under **Advanced settings → Secrets**, add:
   ```toml
   GOOGLE_API_KEY = "your_actual_key_here"
   ```
5. Click **Deploy**.

> Note: The FAISS index is stored locally in the app's container and does not persist across restarts — each new session requires re-uploading and processing the PDF.

---

## 📁 Project Structure

```
pdfQnA/
├── app.py                     # Main Streamlit application
├── requirements.txt           # Python dependencies
├── .env.example                # Sample environment file (rename to .env)
├── .gitignore
├── PROJECT_DOCUMENTATION.md   # Architecture, flowchart, module docs, testing
└── faiss_index/                # Auto-created locally after processing a PDF (gitignored)
```

---

## 🧪 Testing

Basic test cases (PDF extraction, chunking, vector store creation, in-context vs out-of-context Q&A) are documented in [`PROJECT_DOCUMENTATION.md`](./PROJECT_DOCUMENTATION.md#11-testing-section-paste-ready-for-ppt-slides).

---

## ⚠️ Known Limitations

- No persistent storage — each session needs the PDF re-processed after a container restart.
- Works best on text-based PDFs; scanned/image-only PDFs won't extract text without OCR.
- Single-PDF context at a time (no multi-document search yet).

---

## 🔮 Future Improvements

- [ ] Support multiple PDFs at once
- [ ] Persistent vector storage across sessions
- [ ] OCR support for scanned documents
- [ ] Source citations showing which page an answer came from

---

## 📄 License

This project is for educational/academic purposes as part of a B.Tech internship.
