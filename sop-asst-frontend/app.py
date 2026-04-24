"""
Streamlit frontend application for SOP Chatbot.
"""
import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="SOP Support Assistant Bot", layout="wide")
st.title("SOP Support Assistant Bot")

# Sidebar for document upload
with st.sidebar:
    st.header("Document Ingestion")
    uploaded_file = st.file_uploader("Upload an SOP document (PDF or DOCX)", type=["pdf", "docx", "txt"])
    
    if st.button("Process Document"):
        if uploaded_file is not None:
            with st.spinner("Processing document..."):
                try:
                    files = {"file": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
                    response = requests.post(f"{BACKEND_URL}/upload", files=files)
                    if response.status_code == 200:
                        st.success(response.json().get("message", "Document processed successfully!"))
                    else:
                        st.error(f"Error: {response.text}")
                except Exception as e:
                    st.error(f"Connection error: {str(e)}")
        else:
            st.warning("Please upload a file first.")

# Main chat interface


if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if query := st.chat_input("Ask a question about the SOPs..."):
    # Append user message
    st.session_state.messages.append({"role": "user", "content": query})
    with st.chat_message("user"):
        st.markdown(query)
        
    # Call backend
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # Add context (conversation history minus the latest query)
                req_data = {
                    "query": query,
                    "history": st.session_state.messages[:-1]
                }
                
                response = requests.post(f"{BACKEND_URL}/chat", json=req_data)
                if response.status_code == 200:
                    answer = response.json().get("response", "Error generating response.")
                    st.markdown(answer)
                    st.session_state.messages.append({"role": "assistant", "content": answer})
                else:
                    err_msg = f"Backend error: {response.text}"
                    st.error(err_msg)
            except Exception as e:
                st.error(f"Cannot connect to backend: {str(e)}")
