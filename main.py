from openai import OpenAI
import os
import sys

# Read API key from environment variable for security
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    print("ERROR: OPENAI_API_KEY environment variable is not set.\nPlease set it and re-run the script.")
    sys.exit(1)

client = OpenAI(api_key=api_key)

user_input = input("Enter your message: ")
print("\n")
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "user", "content": user_input}
    ]
)

print(response.choices[0].message.content)