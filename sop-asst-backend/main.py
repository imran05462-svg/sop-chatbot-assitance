"""
Main module for the SOP Assistance Chatbot backend.
"""
from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
import sys
import os

# Ensure backend imports work when run as module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from ingestion import process_uploaded_file
from retriever import create_and_save_index, search_documents
from llm import generate_response

app = FastAPI(title="SOP Assistance Chatbot API", version="1.0.0")

from typing import List, Dict

class ChatRequest(BaseModel):
    query: str
    history: List[Dict[str, str]] = []

class ChatResponse(BaseModel):
    response: str

@app.get("/")
def read_root():
    return {"message": "SOP Assistance Chatbot Backend Status: OK"}

@app.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(status_code=400, detail="No filename provided")
        
    try:
        file_bytes = await file.read()
        chunks = process_uploaded_file(file.filename, file_bytes)
        
        if not chunks:
            return {"message": "No text extracted from the document."}
            
        create_and_save_index(chunks)
        return {"message": f"Successfully processed '{file.filename}' and stored {len(chunks)} chunks in FAISS."}
        
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")

@app.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
        
    try:
        # Retrieve context
        context_chunks = search_documents(request.query, top_k=3)
        if not context_chunks:
            context_text = "No SOP context available. Please upload a document first."
        else:
            context_text = "\n\n".join(context_chunks)
            
        # Generate response passing history for memory
        response_text = generate_response(
            query=request.query, 
            context=context_text, 
            history=request.history
        )
        return ChatResponse(response=response_text)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during chat generation: {str(e)}")

if __name__ == "__main__":
    from fastapi.testclient import TestClient
    
    print("Testing FastAPI endpoints using TestClient...")
    client = TestClient(app)
    
    # Test Root
    res = client.get("/")
    assert res.status_code == 200, "Root endpoint failed"
    
    # Test Chat
    chat_res = client.post("/chat", json={"query": "Hello"})
    assert chat_res.status_code == 200, f"Chat endpoint failed: {chat_res.text}"
    
    print("Test responses:")
    print("ROOT:", res.json())
    print("CHAT:", chat_res.json()["response"][:100] + "...")
    print("\nFastAPI logic tested successfully!")
