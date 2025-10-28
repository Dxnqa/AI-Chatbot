import chromadb
import uuid
import os
import logging
from pathlib import Path
from chromadb.utils.embedding_functions import OpenAIEmbeddingFunction
from dotenv import load_dotenv

DIR = Path(__file__).resolve().parent
DB_PATH = DIR / "testing" / "database"
SOURCE_DIR = DIR / "testing" / "Notes"

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s")

class EmbeddingBot:
    def __init__(self, api_key: str, db_path: Path = DB_PATH):
        self.client = chromadb.PersistentClient(path=db_path)
        self.embedding = OpenAIEmbeddingFunction(
            api_key=api_key,
            model_name="text-embedding-3-small"
        )
        self.collection = self.client.get_or_create_collection(
            name="knowledge_base_openai",
            embedding_function=self.embedding
        )

    # Method: collect .txt files from the source directory        
    def collect_files(self, source_dir: Path = SOURCE_DIR) -> list[Path]:
        file_list = []
        file_list.extend(file for file in source_dir.rglob("*.txt") if file.is_file())
        return file_list

    # Method: read file content
    def read_file(self, file_path: Path):
        return file_path.read_text(encoding="utf-8", errors="ignore").strip()

    # Method: chunk text with a limit of 1500 characters. Return list of chunks
    def chunk_text(self, text: str, chunk_size: int = 1500) -> list[str]:
        if chunk_size <= 0:
            raise ValueError("chunk_size must be a positive integer")

        chunks: list[str] = []
        for start_index in range(0, len(text), chunk_size):
            if chunk := text[start_index : start_index + chunk_size]:
                chunks.append(chunk)

        return chunks

    # Method: Create a unique id for each chunk.
    def content_chunk_id(self, chunk: str) -> str:
        if not chunk:
            raise ValueError("Chunk cannot be empty")
        return str(uuid.uuid4().hex)
    
    # Method: Process files for logging. Returns a summary of results.
    def file_processing(self, log_list: list[str]) -> dict[str, int | list[dict[str, str]] | str]:
        results = {
            "status": "success",
            "files_processed": 0,
            "files_skipped": 0,
            "errors": []
        }
        for file in log_list:
            try:
                content = self.read_file(file)
                if not content:
                    logging.warning(f"Empty content in file: {file}")
                    results["files_skipped"] += 1
                else:
                    results["files_processed"] += 1
            except Exception as e:
                logging.exception(f"Failed to read file: {file}")
                results["files_skipped"] += 1
                results["errors"].append({"file": str(file), "error": str(e)})
        return results
    
    # Method: Process embeddings and chunks for logging.
    def embedding_logs(self, chunks: list[str]) -> dict[str, int | list[dict[str, str]] | str]:
        results = {
            "status": "success",
            "chunks_embedded": 0,
            "errors": []
        }
        for chunk in chunks:
            try:
                if not chunk:
                    logging.warning("Empty chunk encountered.")
                    results["errors"].append({"chunk": chunk, "error": "Empty chunk"})
                else:
                    results["chunks_embedded"] += 1
                    logging.info(results["status"])
            except Exception as e:
                logging.exception("Failed to process chunk.")
                results["errors"].append({"chunk": chunk, "error": str(e)})
        return results
    
    # Main Method: Embed chunked pieces from "chunks" => add to collection.
    # For parameter embedding_list: use collect_files() to get list of files.
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