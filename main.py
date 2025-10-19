from openai import OpenAI
from dotenv import load_dotenv
import os
import sys
from Chatbot import ChatBot

# Load API key from .env file. Make sure you have a .env file with OPENAI_API_KEY set.
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("ERROR: OPENAI_API_KEY environment variable is not set.\nPlease set it and re-run the script.")
    sys.exit(1)

client = OpenAI(api_key=api_key)


# Initialize the chatbot object from prompt.py with the OpenAI client
# Conversation array for conversation management
conversation_history = []
chatBot = ChatBot(client)

print("\nType 'exit' to end the conversation.\n")

while True:
    user_input = input("Assistant: How can I help you today?\nPrompt: ")
    if user_input.strip().lower() in {"exit", "quit", "q"}:
        print("Goodbye!")
        break

    conversation_history.append({"role": "user", "content": user_input})

    try:
        response = chatBot.web_search(conversation_history)
    except Exception as error:
        print(f"Assistant: Sorry, something went wrong ({error}). Let's try again.")
        continue

    assistant_reply = response.output_text
    conversation_history.append({"role": "assistant", "content": assistant_reply})

    print(f"\nResponse: {assistant_reply}\n")