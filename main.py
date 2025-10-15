from openai import OpenAI
from dotenv import load_dotenv
import os
import sys

# Load API key from .env file
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("ERROR: OPENAI_API_KEY environment variable is not set.\nPlease set it and re-run the script.")
    sys.exit(1)

client = OpenAI(api_key=api_key)

# Enter user input for prompt
user_input = input("Enter your message: ")
print("\n")

response = client.responses.create(
    include=["web_search_call.action.sources"],
    model="gpt-5",
    tools=[{"type": "web_search"}],
    input=user_input
)

print(f"Response ID: {response.id}")
print(f"Response Output: {response.output_text}")