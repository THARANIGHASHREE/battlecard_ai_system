from fastapi import FastAPI
from backend.data_collection import search_wikipedia

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI!"}

@app.get("/search")
def search(query: str):
    """
    Use Wikipedia API instead of DuckDuckGo.
    Example: /search?query=OpenAI
    """
    result = search_wikipedia(query)
    return result
