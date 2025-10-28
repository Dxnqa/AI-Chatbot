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

class EmbeddingBot:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=DB_PATH)
        self.embedding = OpenAIEmbeddingFunction(
            api_key=api_key,
            model_name="text-embedding-3-small"
        )
        self.collection = self.client.get_or_create_collection(
            name="knowledge_base_openai",
            embedding_function=self.embedding
        )

    # Function to collect .txt files from the source directory        
    def collect_files(self, source_dir: Path = SOURCE_DIR) -> list[Path]:
        file_list = []
        file_list.extend(file for file in source_dir.rglob("*.txt") if file.is_file())
        return file_list

    def read_file(self, file_path: Path):
        return file_path.read_text(encoding="utf-8", errors="ignore").strip()

    # Function: chunk text with a limit of 1500 characters. Return list of chunks
    def chunk_text(self, text: str, chunk_size: int = 1500) -> list[str]:
        if chunk_size <= 0:
            raise ValueError("chunk_size must be a positive integer")

        chunks: list[str] = []
        for start_index in range(0, len(text), chunk_size):
            if chunk := text[start_index : start_index + chunk_size]:
                chunks.append(chunk)

        return chunks

    # Create a unique id for each chunk.
    def content_chunk_id(self, chunk: str) -> str:
        if not chunk:
            raise ValueError("Chunk cannot be empty")
        return str(uuid.uuid4().hex)
    
    def embed_files(self, embedding_list):
        for file in embedding_list:
            content = self.read_file(file)
            chunks = self.chunk_text(content, chunk_size=1500)
            chunk_ids = [f"{file.stem}_{self.content_chunk_id(chunk)}" for chunk in chunks]
            
            self.collection.add(
                documents=chunks,
                ids=chunk_ids,
                metadatas=[{"source_file": file.name} for _ in chunks]
            )