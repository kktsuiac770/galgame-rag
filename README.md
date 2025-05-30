# Galgame Review RAG Service

This project is a Python-based Retrieval-Augmented Generation (RAG) service for galgame reviews. It scrapes comments from erogamescape, stores them in a vector database, and allows user Q&A over the comments using Google Gemini for both embeddings and LLM.

## Features
- Scrape game comments from erogamescape
- Store comments in a ChromaDB vector database
- Use Google Gemini for embeddings and LLM Q&A
- Simple CLI for asking questions about game reviews

## Requirements
- Python 3.9+
- Google Gemini API key
- All dependencies in `requirements.txt`

## Setup
1. Install dependencies:
   ```zsh
   pip install -r requirements.txt
   ```
2. Scrape the game comments and cache them locally:
   ```zsh
   python scraper.py <game_id>
   # Example:
   python scraper.py 33172
   ```
3. Set your Google Gemini API key as an environment variable:
   ```zsh
   export GOOGLE_API_KEY=your-gemini-api-key
   ```
4. Run the service:
   ```zsh
   python main.py <game_id>
   # Example:
   python main.py 33172
   ```

## File Structure
- `main.py` — Main entry point, RAG pipeline
- `scraper.py` — Scrapes comments from erogamescape
- `requirements.txt` — Python dependencies
- `chroma.db/` — Vector database files
- `data/` — Cached or scraped data

## Notes
- On your first run, make sure to uncomment the `create_db()` line in `main.py` to build the vector database. You can comment it out on subsequent runs for faster startup.
- Make sure your Google Gemini API key is valid and has access to embedding and LLM endpoints.
- The service will prompt you for questions and return answers based on the most relevant comments.

## License
MIT
