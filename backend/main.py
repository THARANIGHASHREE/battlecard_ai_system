from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from backend.data_collection import search_wikipedia
from backend.text_analysis import extract_keywords
from backend.insights_generator import generate_insights  # ✅ NEW!

import pdfkit
import io
import os
from jinja2 import Environment, FileSystemLoader

app = FastAPI()

# ✅ Absolute safe paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_path = os.path.join(BASE_DIR, "static")
templates_path = os.path.join(BASE_DIR, "templates")

app.mount("/static", StaticFiles(directory=static_path), name="static")
templates = Jinja2Templates(directory=templates_path)

config = pdfkit.configuration(wkhtmltopdf=r"C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")

@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI!"}

@app.get("/search", response_class=HTMLResponse)
def search(request: Request, query: str):
    result = search_wikipedia(query)
    keywords = extract_keywords(result.get("Extract", ""))
    strengths, weaknesses, differentiators, action = generate_insights(result.get("Extract", ""), keywords)

    return templates.TemplateResponse("battlecard.html", {
        "request": request,
        "title": result.get("Title", ""),
        "extract": result.get("Extract", ""),
        "url": result.get("ContentURL", ""),
        "keywords": keywords,
        "strengths": strengths,
        "weaknesses": weaknesses,
        "differentiators": differentiators,
        "action": action
    })

@app.get("/download")
def download(query: str):
    result = search_wikipedia(query)
    keywords = extract_keywords(result.get("Extract", ""))
    strengths, weaknesses, differentiators, action = generate_insights(result.get("Extract", ""), keywords)

    env = Environment(loader=FileSystemLoader("backend/templates"))
    template = env.get_template("battlecard.html")
    html_content = template.render(
        title=result.get("Title", ""),
        extract=result.get("Extract", ""),
        url=result.get("ContentURL", ""),
        keywords=keywords,
        strengths=strengths,
        weaknesses=weaknesses,
        differentiators=differentiators,
        action=action
    )

    pdf = pdfkit.from_string(
        html_content,
        False,
        configuration=config,
        options={"enable-local-file-access": ""}
    )

    return StreamingResponse(io.BytesIO(pdf), media_type="application/pdf", headers={
        "Content-Disposition": f"attachment; filename={query}_battlecard.pdf"
    })
