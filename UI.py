import streamlit as st
import requests
import os
import sys

# -----------------------------
# Helper Functions
# -----------------------------
def analyze_resume_ui(query):
    """Send query to Flask backend and get response"""
    try:
        res = requests.post(
            "http://127.0.0.1:5000/analyze",
            json={"query": query},
            timeout=30
        )
        res_json = res.json()
        if "error" in res_json:
            return f"❌ Error: {res_json['error']}"
        else:
            return res_json["response"]
    except requests.exceptions.ConnectionError:
        return "❌ Cannot connect to backend. Make sure Flask server is running on port 5000."
    except Exception as e:
        return f"❌ Error: {str(e)}"

def get_sample_questions():
    return [
        "Summarize the key skills and experience",
        "What are the main technical skills?",
        "Describe the work experience",
        "What projects are mentioned?",
        "What is the educational background?",
        "List all programming languages and tools",
    ]

# -----------------------------
# Streamlit UI Setup
# -----------------------------
st.set_page_config(
    page_title="🎯 Resume Analysis Chatbot",
    page_icon="🤖",
    layout="wide",
)

st.markdown(
    """
    <style>
    .main {
        background: linear-gradient(135deg, #f6f9fc 0%, #eef2f3 100%);
    }
    div.stButton > button {
        width: 100%;
        border-radius: 8px;
        font-weight: 600;
        padding: 0.6em 0;
    }
    .stChatMessage {
        border-radius: 10px;
        padding: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🎯 Resume Analysis Chatbot")
st.caption("Powered by AI — Ask anything about the resume!")

# Initialize chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:
    st.header("💡 Sample Questions")
    for q in get_sample_questions():
        if st.button(q):
            st.session_state["sample_question"] = q
            st.experimental_rerun()

    st.markdown("---")
    st.subheader("📋 Tips")
    st.markdown("""
    - Be specific in your questions  
    - Ask about skills, experience, projects, or education  
    - You can ask follow-up questions  
    """)

    st.markdown("---")
    st.subheader("⚙️ Backend Status")
    st.code("python resume.py", language="bash")
    if st.button("🗑️ Clear Chat"):
        st.session_state.chat_history = []
        st.session_state["sample_question"] = ""
        st.experimental_rerun()

# -----------------------------
# Main Chat Section
# -----------------------------
for msg in st.session_state.chat_history:
    role = "user" if msg["role"] == "user" else "assistant"
    with st.chat_message(role):
        st.markdown(msg["content"])

# -----------------------------
# Chat Input
# -----------------------------
if prompt := st.chat_input("Ask about the resume..."):
    st.session_state.chat_history.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = analyze_resume_ui(prompt)
            st.markdown(response)
    st.session_state.chat_history.append({"role": "assistant", "content": response})

# Auto-fill sample question from sidebar
if "sample_question" in st.session_state and st.session_state["sample_question"]:
    q = st.session_state["sample_question"]
    st.session_state.chat_history.append({"role": "user", "content": q})
    with st.chat_message("user"):
        st.markdown(q)

    with st.chat_message("assistant"):
        with st.spinner("Analyzing..."):
            response = analyze_resume_ui(q)
            st.markdown(response)
    st.session_state.chat_history.append({"role": "assistant", "content": response})
    st.session_state["sample_question"] = ""
    st.experimental_rerun()

# -----------------------------
# Optional Launcher with Port
# -----------------------------
if __name__ == "__main__":
    port = 7000  # 👈 Change this to your desired port
    os.system(f"streamlit run {sys.argv[0]} --server.port={port}")
