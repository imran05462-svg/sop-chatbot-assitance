"""
Retriever logic for searching FAISS using Hugging Face embeddings.
"""
import os
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from typing import List, Tuple, Optional

INDEX_FILE = "faiss_index.bin"
MAPPING_FILE = "chunk_mapping.json"
EMBEDDING_DIM = 384  # Dimension for all-MiniLM-L6-v2

# Initialize SentenceTransformer model locally
embedder = SentenceTransformer('all-MiniLM-L6-v2')

def get_embeddings(texts: List[str]) -> np.ndarray:
    """Generate embeddings for a list of texts using Hugging Face model locally."""
    embeddings = embedder.encode(texts)
    return np.array(embeddings).astype('float32')

def get_embedding(text: str) -> np.ndarray:
    """Generate embedding for a single text using Hugging Face model locally."""
    embedding = embedder.encode([text])
    return np.array(embedding).astype('float32')

def create_and_save_index(chunks: List[str]):
    """Create FAISS index from chunks and save to disk."""
    if not chunks:
        return
        
    embeddings = get_embeddings(chunks)
    dimension = embeddings.shape[1]
    
    # Create L2 index
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)
    
    # Save index
    faiss.write_index(index, INDEX_FILE)
    
    # Save text mapping
    with open(MAPPING_FILE, "w", encoding="utf-8") as f:
        json.dump(chunks, f)

def load_index() -> Tuple[Optional[faiss.IndexFlatL2], Optional[List[str]]]:
    """Load FAISS index and chunk mappings."""
    if not os.path.exists(INDEX_FILE) or not os.path.exists(MAPPING_FILE):
        return None, None
        
    index = faiss.read_index(INDEX_FILE)
    with open(MAPPING_FILE, "r", encoding="utf-8") as f:
        chunks = json.load(f)
        
    return index, chunks

def search_documents(query: str, top_k: int = 3) -> List[str]:
    """Retrieve top_k chunks matching the query from existing FAISS index."""
    index, chunks = load_index()
    if index is None or chunks is None:
        return []
        
    query_embedding = get_embedding(query)
    
    top_k = min(top_k, index.ntotal)
    if top_k == 0:
        return []

    distances, indices = index.search(query_embedding, top_k)
    
    results = []
    for idx in indices[0]:
        if idx != -1 and idx < len(chunks):
            results.append(chunks[idx])
            
    return results

if __name__ == "__main__":
    # Test FAISS index creation and search
    test_chunks = [
        "First step is to reboot the system.",
        "To escalate, notify the Level 3 team via Jira.",
        "Check the logs located at /var/log/syslog."
    ]
    create_and_save_index(test_chunks)
    print("Index created and saved.")
    
    results = search_documents("How to check logs?", top_k=2)
    print("Search results:")
    for res in results:
        print("-", res)
    print("FAISS Embeddings and retrieval tested successfully using Hugging Face!")
