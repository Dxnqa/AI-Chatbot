import chromadb
import uuid
import os
from pathlib import Path
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction

DIR = Path(__file__).resolve().parent
DB_PATH = DIR / "testing" / "database"
SOURCE_DIR = DIR / "testing" / "Notes"

documents = []
metadata = []
ids = []

# client = chromadb.PersistentClient(path=DB_PATH)
# embedding = OpenAIEmbeddingFunction(
#     api_key=os.getenv("OPENAI_API_KEY"),
#     model_name="text-embedding-3-small"
#     )


# collection = client.get_or_create_collection(
#     name="knowledge_base",
#     embedding_function=embedding)
        
def embed_list(file_list):
    for file in SOURCE_DIR.glob("*/*"):
        if file.is_file() and file.suffix.lower() == ".txt":
            file_list.append(file)
    return file_list

embed_list(documents)
