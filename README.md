# 🎯 Resume Analyzer RAG Project

An **AI-powered Resume Analyzer Chatbot** built using **Retrieval-Augmented Generation (RAG)**, combining **Flask** (for backend) and **Streamlit** (for frontend) to interactively analyze resumes and answer user queries based on resume content.

---

## 🧠 Project Overview

This project enables users to upload or use a preloaded resume and ask natural language questions such as:  
- “Summarize the key skills and experience.”  
- “What projects are mentioned?”  
- “What is the educational background?”  

The chatbot uses **LangChain**, **HuggingFace Embeddings**, **FAISS**, and **Groq’s Llama3 model** to extract, embed, and retrieve contextually relevant information from the resume.

---

## ⚙️ Tech Stack

| Component | Technology Used |
|------------|-----------------|
| Backend | Flask |
| Frontend | Streamlit |
| LLM | Groq Llama3 (via ChatGroq API) |
| Embeddings | HuggingFace MiniLM-L6-v2 |
| Vector Store | FAISS |
| Document Parsing | PyPDF2 |
| Environment Management | Python-dotenv |
| Framework | LangChain (for RAG Pipeline) |

---

## 🧩 Backend – Flask (resume.py)

The backend is responsible for:
- Extracting text from a **PDF resume** using `PyPDF2`
- Splitting text into manageable chunks using `RecursiveCharacterTextSplitter`
- Generating vector embeddings using `HuggingFaceEmbeddings`
- Storing and retrieving chunks via **FAISS**
- Using **ChatGroq (Llama3)** for context-based Q&A
- Providing REST APIs for the Streamlit UI

### 📍 Flask Endpoints
| Endpoint | Method | Description |
|-----------|---------|-------------|
| `/analyze` | POST | Takes a question and returns an AI-generated answer based on the resume |
| `/health` | GET | Health check for backend |

### 🧮 RAG Workflow
1. Resume text is split into chunks (`chunk_size=500`, `chunk_overlap=50`).  
2. Each chunk is embedded into a vector space using **MiniLM**.  
3. When a question is asked, relevant chunks are retrieved via **FAISS**.  
4. The retrieved context and question are passed to **Groq Llama3** for response generation.

---

## 💬 Frontend – Streamlit (streamlit_app.py)

The Streamlit app serves as the user interface, providing:
- A **chat-style layout** to ask resume-related questions
- **Sidebar** with sample prompts (skills, experience, projects, etc.)
- **Backend connection check**
- **Chat history** and **reset** button

### 🖥️ Features
✅ Real-time resume Q&A  
✅ Predefined sample questions  
✅ Dynamic chat interface  
✅ Error handling for backend connection  
✅ Simple and modern UI design  

📂 Project Structure
bash
Copy code
Resume_Analyzer_RAG_GenAI/
│
├── resume.py                # Flask backend (RAG logic)
├── streamlit_app.py         # Streamlit frontend
├── Resume_JainSuyasha.pdf   # Sample resume
├── .env                     # API keys (ignored by Git)
├── requirements.txt         # Dependencies
└── README.md                # Documentation
✨ Key Highlights
Integrates LangChain, FAISS, and Groq LLM

Full-stack integration between Flask and Streamlit

Modular and extensible architecture

Smooth real-time chat for resume insights

👩‍💻 Author
Suyasha Jain (Suyasha28)
Associate Data Engineer | Data Analyst | AI Enthusiast

📧 Email: suyashajain415@gmail.com
🌐 GitHub: github.com/Suyasha28

