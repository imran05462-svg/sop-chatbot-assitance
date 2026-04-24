"""
LLM integration using Hugging Face Inference API (free tier).
"""
import os
from huggingface_hub import InferenceClient
from dotenv import load_dotenv

load_dotenv()

# Configure HuggingFace
hf_token = os.getenv("HF_API_KEY", "")

# Free serverless inference model
MODEL_NAME = "meta-llama/Meta-Llama-3-8B-Instruct"

client = InferenceClient(
    model=MODEL_NAME,
    token=hf_token if hf_token else None,
)

SYSTEM_PROMPT = """You are a SOP Support Assistant Bot.

STRICT INSTRUCTIONS:
- Use ONLY the SOP context provided below.
- Do NOT use prior knowledge.
- Do NOT hallucinate or assume missing details.

OUT-OF-SCOPE HANDLING:
- If the user question is NOT related to the provided SOP context,
  OR if the retrieved context does NOT contain enough information to answer,
  respond ONLY with:
  "This question does not belong to the provided document."

- Do NOT attempt to answer in such cases.
- Do NOT generate partial or guessed responses.

WHEN CONTEXT IS VALID:
- Provide accurate, step-by-step solutions strictly from context.
- If the query is vague, ask a clarifying question.

Structure your response with these exact headers:
## Problem Understanding
## Resolution Steps
## Verification
## Escalation

SOP Context:
{context}
"""

def generate_response(query: str, context: str, history: list = None) -> str:
    """Generate a structured response using Hugging Face Inference API."""
    if history is None:
        history = []

    # Build messages array
    messages = [{"role": "system", "content": SYSTEM_PROMPT.format(context=context)}]

    # Add last 6 turns of history
    for msg in history[-6:]:
        role = msg.get("role", "user")
        if role == "model":
            role = "assistant"
        if role not in ["user", "assistant"]:
            role = "user"
        messages.append({"role": role, "content": msg.get("content", "")})

    # Add current user query
    messages.append({"role": "user", "content": query})

    try:
        response = client.chat_completion(
            messages=messages,
            max_tokens=1024,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"**Error from Hugging Face API:** {str(e)}"

if __name__ == "__main__":
    sample_context = "- Reboot the system.\n- Notify Level 3 team via Jira if it fails."
    sample_query = "What happens if reboot fails?"
    print("Testing generate_response with HuggingFace...")
    result = generate_response(sample_query, sample_context)
    print("Response Generated:\n")
    print(result)
    print("\nHuggingFace LLM Logic tested successfully!")
