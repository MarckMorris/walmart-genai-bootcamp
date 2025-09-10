# main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, List
import asyncio
import ollama
import os

# Pydantic model to define the request body structure
class PromptRequest(BaseModel):
    prompt: str

# Create an Ollama client instance that connects to the host machine.
# This is necessary because the Docker container runs in an isolated network.
ollama_client = ollama.Client(host='http://host.docker.internal:11434')

# Instance of the FastAPI application
app = FastAPI(
    title="Walmart GenAI API",
    description="A GenAI service powered by a local LLM for various tasks."
)

# --- Reusing the Product class from Day 1 ---
class Product:
    def __init__(self, product_id: str, name: str, price: float):
        self.product_id = product_id
        self.name = name
        self.price = price

    async def get_details(self) -> Dict:
        print(f"Fetching details for product {self.product_id}...")
        await asyncio.sleep(0.5)
        return {
            "product_id": self.product_id,
            "name": self.name,
            "price": self.price,
            "status": "Available"
        }
# -----------------------------------------------

# Function to retrieve relevant documents (simple search for now)
def retrieve_documents(query: str, file_path: str = 'walmart_policies.txt') -> str:
    """
    Simulates retrieving documents based on a keyword search.
    """
    relevant_docs = []
    # Check if the file exists within the container
    if not os.path.exists(file_path):
        return "No policies found."

    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
        # A simple way to split documents is by double newlines
        documents = content.strip().split('\n\n')

        # Simple keyword matching for retrieval
        for doc in documents:
            if any(keyword.lower() in doc.lower() for keyword in query.split()):
                relevant_docs.append(doc)

    return "\n\n".join(relevant_docs) if relevant_docs else "No relevant information found."


# Define a simple GET endpoint
@app.get("/product/{product_id}", response_model=Dict)
async def get_product(product_id: str):
    mock_db = {
        "12345": Product(product_id="12345", name="Lego Set", price=49.99),
        "67890": Product(product_id="67890", name="Echo Dot", price=39.99),
    }
    product = mock_db.get(product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    details = await product.get_details()
    return details

# Define the POST endpoint for basic LLM interaction
@app.post("/ask", response_model=Dict)
async def ask_llm(request: PromptRequest):
    print(f"Received simple prompt: {request.prompt}")
    messages = [
        {'role': 'system', 'content': 'You are a helpful and professional Walmart GenAI assistant.'},
        {'role': 'user', 'content': request.prompt}
    ]
    response = ollama_client.chat(model='llama3', messages=messages)
    return {
        "prompt": request.prompt,
        "response": response['message']['content']
    }

# Define the new POST endpoint for RAG
@app.post("/ask_rag", response_model=Dict)
async def ask_rag(request: PromptRequest):
    print(f"Received RAG prompt: {request.prompt}")

    # Step 1: Retrieval
    relevant_context = retrieve_documents(request.prompt)

    # Step 2: Augmentation (Create an enriched prompt)
    full_prompt = f"""
    Based on the following context, answer the user's question. If the answer is not in the context, state that you cannot answer.

    Context:
    ---
    {relevant_context}
    ---

    User's question: {request.prompt}
    """

    messages = [
        {'role': 'system', 'content': 'You are a helpful and professional Walmart GenAI assistant. Answer strictly based on the provided context.'},
        {'role': 'user', 'content': full_prompt}
    ]

    # Step 3: Generation
    response = ollama_client.chat(model='llama3', messages=messages)

    return {
        "prompt": request.prompt,
        "response": response['message']['content'],
        "context_used": relevant_context
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)