**What is FAISS?**

Meta developed FAISS (Facebook AI Similarity Search) — a library used for:

storing vector embeddings
similarity search
nearest neighbor search
fast retrieval in AI/RAG systems

It is widely used in:

Chatbots
RAG pipelines
Semantic search
Recommendation systems
Image similarity search
**Simple Understanding**

FAISS helps find:

“Which stored data is most similar to my query?”

Instead of keyword matching, it uses vector similarity.

**Example**

Suppose you have documents:

1. Password reset SOP
2. VPN troubleshooting
3. Account unlock process

After embedding conversion:

Password reset → [0.12, -0.44, 0.91 ...]
VPN issue      → [0.33,  0.22, 0.11 ...]

FAISS stores these vectors.

When user asks:

"I forgot my password"

FAISS finds the closest vector:
→ "Password reset SOP"
