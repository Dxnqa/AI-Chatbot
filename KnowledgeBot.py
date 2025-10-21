from unittest import result
from openai import OpenAI
from io import BytesIO
import os
import requests

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Class to handle file options using OpenAI APIs
class FileOptions:
    def __init__(self, client):
        self.client = client
        
    # Method to create a file from a local path or URL
    def create_file(self, file_path):
        if file_path.startswith("http://") or file_path.startswith("https://"):
            # Download the file content from the URL
            response = requests.get(file_path)
            file_content = BytesIO(response.content)
            file_name = file_path.split("/")[-1]
            file_tuple = (file_name, file_content)
            result = client.files.create(
                file=file_tuple,
                purpose="assistants"
            )
        else:
            # Handle local file path
            with open(file_path, "rb") as file_content:
                result = client.files.create(
                    file=file_content,
                    purpose="assistants"
                )
        print(result.id)
        return result.id

vector_storage = client.vector_stores.create(
    name="Knowledge Base"
)