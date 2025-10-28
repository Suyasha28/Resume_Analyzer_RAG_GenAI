import os
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq
from flask import Flask, request, jsonify
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Load environment variables
load_dotenv()

# Extract text from PDF
def extract_resume_text(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PdfReader(file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return text.strip()

# Prepare RAG components
def setup_rag(resume_text):
    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=35)
    chunks = text_splitter.split_text(resume_text)
    
    # Generate embeddings and vector store
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vector_store = FAISS.from_texts(chunks, embeddings)
    
    # Initialize Groq LLM
    llm = ChatGroq(api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.1-8b-instant")

    # Create retriever
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    
    # Create prompt template
    template = """Answer the question based only on the following context from the resume:

Context: {context}

Question: {question}

Answer:"""
    
    prompt = ChatPromptTemplate.from_template(template)
    
    # Helper function to format documents
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)
    
    # Create RAG chain using LCEL (LangChain Expression Language)
    rag_chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    return rag_chain

# Flask API
app = Flask(__name__)

# Load resume and RAG on startup
resume_text = extract_resume_text(r"C:\Users\asus\OneDrive\Desktop\GEN_AI\Resume_JainSuyasha.pdf")
rag_chain = setup_rag(resume_text)

@app.route('/analyze', methods=['POST'])
def analyze_resume():
    query = request.json.get('query')
    if not query:
        return jsonify({"error": "No query provided"}), 400
    
    try:
        response = rag_chain.invoke(query)
        return jsonify({"response": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500 

@app.route('/')
def home():
    return """
    <h2>Resume Q&A API is running ✅</h2>
    <p>Use <b>/analyze</b> (POST) to ask questions about the resume.</p>
    <p>Example JSON body:</p>
    <pre>{
        "query": "What are Suyasha's key skills?"
    }</pre>
    """


@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy"})

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)