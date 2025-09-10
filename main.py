# main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List
import ollama

# Pydantic model to define the request body structure for asking questions
class PromptRequest(BaseModel):
    prompt: str

# Create an Ollama client instance that connects to the host machine.
# This is necessary because the Docker container runs in an isolated network.
# 'host.docker.internal' is a special DNS name that resolves to the host's IP.
ollama_client = ollama.Client(host='http://host.docker.internal:11434')

# Instance of the FastAPI application
app = FastAPI(
    title="Walmart GenAI API",
    description="A GenAI service powered by a local LLM for various tasks."
)

# --- INICIO: NUEVO CÓDIGO PARA SOLUCIONAR EL ERROR CORS ---
origins = ["*"]  # Permite solicitudes desde cualquier origen

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los encabezados
)
# --- FIN: NUEVO CÓDIGO ---

@app.get("/")
def read_root():
    return {"message": "Welcome to the Walmart GenAI API!"}

@app.post("/ask", response_model=Dict)
async def ask_llm(request: PromptRequest):
    """
    Sends a prompt to the locally-hosted LLM and returns the generated response.
    This endpoint does NOT use Retrieval-Augmented Generation (RAG).
    """
    print(f"Received prompt for /ask: {request.prompt}")
    
    try:
        # Use a system prompt to give the LLM a professional persona
        messages = [
            {'role': 'system', 'content': 'You are a helpful and professional Walmart GenAI assistant.'},
            {'role': 'user', 'content': request.prompt}
        ]
        
        # Call the local Ollama LLM using the configured client
        response = ollama_client.chat(model='llama3', messages=messages)
        
        return {
            "prompt": request.prompt,
            "response": response['message']['content']
        }
    except Exception as e:
        print(f"Error calling Ollama: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error: Could not connect to the LLM.")

@app.post("/ask_rag", response_model=Dict)
async def ask_with_rag(request: PromptRequest):
    """
    Uses Retrieval-Augmented Generation (RAG) to answer questions based on a specific knowledge base.
    """
    print(f"Received prompt for /ask_rag: {request.prompt}")
    
    # 1. Load the knowledge base from a file
    # In a real-world app, this would be a database or a vector store
    try:
        with open("walmart_policies.txt", "r", encoding="utf-8") as file:
            knowledge_base = file.read()
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Knowledge base file not found.")

    # 2. Split the knowledge base into manageable "chunks" for processing
    chunks = knowledge_base.split("\n\n")

    # 3. Create a query embedding for the user's prompt
    # Embeddings convert text into a numerical vector that represents its meaning.
    query_embedding = ollama_client.embeddings(model="mxbai-embed-large", prompt=request.prompt)['embedding']
    
    # 4. Find the most relevant chunk(s) from the knowledge base using vector similarity
    # We will use the dot product for a simple similarity search.
    # In a production app, a dedicated vector database would handle this more efficiently.
    relevant_chunks = []
    
    for chunk in chunks:
        # Get the embedding for each chunk of text
        chunk_embedding = ollama_client.embeddings(model="mxbai-embed-large", prompt=chunk)['embedding']
        
        # Calculate the dot product (a measure of similarity)
        dot_product = sum(a * b for a, b in zip(query_embedding, chunk_embedding))
        
        # Simple check: if similarity is above a certain threshold, consider it relevant
        if dot_product > 0.6:  # This threshold can be adjusted
            relevant_chunks.append(chunk)

    # 5. Build the final prompt for the LLM using the retrieved context
    context = "\n".join(relevant_chunks)
    prompt_with_context = f"""
    Based on the following information, answer the user's question.
    If the information does not contain the answer, say "I could not find the answer in the provided context."

    Context:
    {context}

    Question:
    {request.prompt}
    """

    # 6. Send the final prompt to the LLM
    try:
        messages = [
            {'role': 'user', 'content': prompt_with_context}
        ]
        response = ollama_client.chat(model='llama3', messages=messages)
        
        return {
            "prompt": request.prompt,
            "response": response['message']['content'],
            "context_used": context
        }
    except Exception as e:
        print(f"Error calling Ollama: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error: Could not connect to the LLM.")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)