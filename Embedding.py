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

# Create a unique id for each chunk.
def content_chunk_id(chunk: str) -> str:
    if not chunk:
        raise ValueError("Chunk cannot be empty")
    return str(uuid.uuid4().hex)

# Main function: Embed chunked pieces from "chunks" => add to collection.
def embed_files(embedding_list):
    for file in embedding_list:    
            content = read_file(file)
            chunks = chunk_text(content, chunk_size=1500)
            chunk_ids = [f"{file.stem}_{content_chunk_id(chunk)}" for chunk in chunks]

            collection.add(
                documents=chunks,
                ids=chunk_ids)

# embed_files(file_list)
print(f"Collection count: {collection.count()}")
print(f"File list length: {len(file_list)}")
print("----------------------------------------------------\n")
user_query = input("Enter your query: ")


context = collection.query(
    query_texts=[user_query],
    n_results=1
    )["documents"][0]
print("\nContext results:\n")
for i, doc in enumerate(context, start=1):
    print(f"{i}. {doc}\n")
print("----------------------------------------------------\n")