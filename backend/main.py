from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from backend.data_collection import search_wikipedia
from backend.text_analysis import extract_keywords

app = FastAPI()
templates = Jinja2Templates(directory="backend/templates")

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI!"}

@app.get("/search", response_class=HTMLResponse)
def search(request: Request, query: str):
    result = search_wikipedia(query)
    keywords = extract_keywords(result.get("Extract", ""))
    return templates.TemplateResponse("battlecard.html", {
        "request": request,
        "title": result.get("Title", ""),
        "extract": result.get("Extract", ""),
        "url": result.get("ContentURL", ""),
        "keywords": keywords
    })
