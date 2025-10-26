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
        
def collect_files(source_dir: Path = SOURCE_DIR) -> list[Path]:
    file_list = []
    file_list.extend(file for file in source_dir.rglob("*.txt") if file.is_file())
    return file_list

def read_file(file_path: Path):
    return file_path.read_text(encoding="utf-8", errors="ignore").strip()


def chunk_text(text: str, chunk_size: int = 1500) -> list[str]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be a positive integer")

    chunks: list[str] = []
    for start_index in range(0, len(text), chunk_size):
        if chunk := text[start_index : start_index + chunk_size]:
            chunks.append(chunk)


    return chunks

documents = collect_files()
chunked_text = chunk_text(read_file(documents[1]), chunk_size=500)
print(f"{documents[1]} Chunked:\n")
print(f"Chunked text (first 3 chunks): {chunked_text[:3]}\n")
print(f"\nRaw: {read_file(documents[1])}\n")