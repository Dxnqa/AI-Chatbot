import chromadb
import uuid
import os

DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(DIR, "testing\\database\\")

print(DB_PATH)

client = chromadb.PersistentClient(path=DB_PATH)
collection = client.get_or_create_collection(name="knowledge_base")

documents = []