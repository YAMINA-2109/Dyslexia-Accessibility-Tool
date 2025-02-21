import requests
import json

# Define Ollama's local API endpoint
OLLAMA_URL = "http://localhost:11434/v1/chat/completions"

def chat_with_granite(prompt):
    # Define request payload
    payload = {
        "model": "granite3.1-dense:2b",
        "messages": [{"role": "user", "content": prompt}]
    }

    # Send POST request to Ollama's API
    response = requests.post(OLLAMA_URL, json=payload)

    # Parse and return response
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.text}"

# Example usage
if __name__ == "__main__":
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            break
        response = chat_with_granite(user_input)
        print(f"Granite: {response}")
