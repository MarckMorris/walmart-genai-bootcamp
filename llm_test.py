# llm_test.py

import ollama

# This function demonstrates a basic call to the LLM
def generate_response(prompt: str) -> str:
    """
    Generates a response from the Llama 3 model using a simple prompt.
    """
    print(f"Sending prompt to LLM: '{prompt}'")
    response = ollama.chat(model='llama3', messages=[
        {'role': 'user', 'content': prompt}
    ])
    return response['message']['content']

# This function shows a more advanced prompt with a specific role
def generate_hr_response(question: str) -> str:
    """
    Generates a response from the LLM, acting as an HR assistant.
    This demonstrates role-based prompting.
    """
    print(f"Sending question to HR Assistant: '{question}'")
    response = ollama.chat(model='llama3', messages=[
        {'role': 'system', 'content': 'You are a helpful and polite HR assistant for Walmart. Your goal is to answer questions about company policies, holidays, and benefits.'},
        {'role': 'user', 'content': question}
    ])
    return response['message']['content']

if __name__ == "__main__":
    # Example 1: Simple prompt
    simple_question = "What is the importance of customer service in retail?"
    answer_1 = generate_response(simple_question)
    print("\n--- Simple Prompt Response ---")
    print(answer_1)

    # Example 2: Role-based prompt for HR
    hr_question = "What is Walmart's policy on remote work?"
    answer_2 = generate_hr_response(hr_question)
    print("\n--- HR Assistant Response ---")
    print(answer_2)