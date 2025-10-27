import chromadb
import uuid
import os
from pathlib import Path
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from dotenv import load_dotenv

DIR = Path(__file__).resolve().parent
DB_PATH = DIR / "testing" / "database"
SOURCE_DIR = DIR / "testing" / "Notes"

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

documents = []
metadata = []
ids = []

client = chromadb.PersistentClient(path=DB_PATH)
embedding = OpenAIEmbeddingFunction(
    api_key=api_key,
    model_name="text-embedding-3-small"
    )


collection = client.get_or_create_collection(
    name="knowledge_base_openai",
    embedding_function=embedding)


# Function to collect .txt files from the source directory        
def collect_files(source_dir: Path = SOURCE_DIR) -> list[Path]:
    file_list = []
    file_list.extend(file for file in source_dir.rglob("*.txt") if file.is_file())
    return file_list

def read_file(file_path: Path):
    return file_path.read_text(encoding="utf-8", errors="ignore").strip()

# Function: chunk text with a limit of 1500 characters. Return list of chunks
def chunk_text(text: str, chunk_size: int = 1500) -> list[str]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be a positive integer")

    chunks: list[str] = []
    for start_index in range(0, len(text), chunk_size):
        if chunk := text[start_index : start_index + chunk_size]:
            chunks.append(chunk)


    return chunks

file_list = collect_files()

# Main function: Embed chunked pieces from "chunks" => add to collection.
def embed_files(embedding_list):
    for file in embedding_list:
        content = read_file(file)
        chunks = chunk_text(content, chunk_size=1500)
        
        collection.add(
            documents=chunks,
            ids=[str(uuid.uuid4()) for _ in chunks])

embed_files(file_list)
print(collection.count())
print(len(file_list))