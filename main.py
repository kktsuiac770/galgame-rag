import scraper
import chromadb
from google import genai
import sys
from dotenv import load_dotenv
import os

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    print("GOOGLE_API_KEY not found in environment variables.")
    sys.exit(1)
google_client = genai.Client(api_key=GOOGLE_API_KEY)
EMBEDDING_MODEL = "gemini-embedding-exp-03-07"
LLM_MODEL = "gemini-2.0-flash"

chromadb_client = chromadb.PersistentClient("./chroma.db")
chromadb_collection = chromadb_client.get_or_create_collection("test_collection")

def embed(text: str, store: bool) -> list[float]:
    result = google_client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text,
        config={
            "task_type": "RETRIEVAL_DOCUMENT" if store else "RETRIEVAL_QUERY"
        }
    )

    assert result.embeddings
    assert result.embeddings[0].values
    return result.embeddings[0].values

def create_db() -> None:
    for idx, c in enumerate(scraper.get_comments("33172")):
        print(f"Process: {c}")
        embedding = embed(c, store=True)
        chromadb_collection.upsert(
            ids=str(idx),
            documents=c,
            embeddings=embedding
        )

def query_db(question: str) -> list[str]:
    question_embedding = embed(question, store=False)
    result = chromadb_collection.query(
        query_embeddings=question_embedding,
        n_results=5
    )
    assert result["documents"]
    return result["documents"][0]


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Usage: python main.py <game_id>")
        sys.exit(1)
    game_id = sys.argv[1]

    question = "What is the main theme of the story?"
    # create_db()
    chunks = query_db(question)
    prompt = "Please answer user's question according to context\n"
    prompt += f"Question: {question}\n"
    prompt += "Context:\n"
    for c in chunks:
        prompt += f"{c}\n"
        prompt += "-------------\n"
    
    result = google_client.models.generate_content(
        model=LLM_MODEL,
        contents=prompt
    )
    print(result.candidates[0].content.parts[0].text.strip())