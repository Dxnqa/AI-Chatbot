from dotenv import load_dotenv
import os
import sys
from pathlib import Path
from EmbeddingBot import EmbeddingBot

DIR = Path(__file__).resolve().parent
DB_PATH = DIR / "testing" / "database"
SOURCE_DIR = DIR / "testing" / "Notes"

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("ERROR: OPENAI_API_KEY environment variable is not set.\nPlease set it and re-run the script.")
    sys.exit(1)
    
embedding_bot = EmbeddingBot(api_key=api_key, db_path=DB_PATH)

collect_files = embedding_bot.collect_files(source_dir=SOURCE_DIR)

# embedding_logs = embedding_bot.embed_files(collect_files)

while True:
    print(f"\nCollection count: {embedding_bot.collection.count()}")
    print("----------------------------------------------------\n")
    user_query = input("Enter your query: ")
    if user_query.strip().lower() in {"/exit", "exit", "quit", "q"}:
        print("Goodbye!")
        break

    context = embedding_bot.query_collection(query_text=user_query, n_results=1).get("documents", [])[0]

    response =  embedding_bot.llm_response(prompt=user_query, context=context[0])

    print("----------------------------------------------------\n")
    print(f"LLM Response:\n\n{response.output_text}\n")
    print("----------------------------------------------------\n")
    
# print("\nContext results:\n")
# for i, doc in enumerate(context, start=1):
#     print(f"{i}. {doc}")