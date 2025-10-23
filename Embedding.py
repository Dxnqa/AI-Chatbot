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

documents = collect_files()
print(documents[2].read_text(encoding="utf-8", errors="ignore"))