from openai import OpenAI
from dotenv import load_dotenv
import os
import sys

# Load API key from .env file. Make sure you have a .env file with OPENAI_API_KEY set.
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("ERROR: OPENAI_API_KEY environment variable is not set.\nPlease set it and re-run the script.")
    sys.exit(1)

client = OpenAI(api_key=api_key)

# Enter user input for prompt
user_input = input("Enter your message: ")
print("\n")

# Response API: fetch response with web search tool
response = client.responses.create(
    include=["web_search_call.action.sources"],
    model="gpt-5",
    tools=[{"type": "web_search"}],
    input=user_input
)

# Print response ID and output text
print(f"Response ID: {response.id}")
print(f"Response Output: {response.output_text}")