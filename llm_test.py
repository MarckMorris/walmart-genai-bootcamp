# llm_test.py

import ollama

# Create a client instance that connects to localhost (default behavior)
# This is for local testing outside of Docker.
ollama_client = ollama.Client(host='http://localhost:11434')

def generate_response(prompt: str) -> str:
    print(f"Sending prompt to LLM: '{prompt}'")
    response = ollama_client.chat(model='llama3', messages=[
        {'role': 'user', 'content': prompt}
    ])
    return response['message']['content']

def generate_hr_response(question: str) -> str:
    print(f"Sending question to HR Assistant: '{question}'")
    response = ollama_client.chat(model='llama3', messages=[
        {'role': 'system', 'content': 'You are a helpful and polite HR assistant for Walmart. Your goal is to answer questions about company policies, holidays, and benefits.'},
        {'role': 'user', 'content': question}
    ])
    return response['message']['content']

if __name__ == "__main__":
    simple_question = "What is the importance of customer service in retail?"
    answer_1 = generate_response(simple_question)
    print("\n--- Simple Prompt Response ---")
    print(answer_1)

    hr_question = "What is Walmart's policy on remote work?"
    answer_2 = generate_hr_response(hr_question)
    print("\n--- HR Assistant Response ---")
    print(answer_2)