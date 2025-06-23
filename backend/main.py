from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from backend.data_collection import search_wikipedia
from backend.text_analysis import extract_keywords

import pdfkit
import io
import os  # ✅ Needed for safe paths
from jinja2 import Environment, FileSystemLoader

app = FastAPI()

# ✅ Bulletproof path handling
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_path = os.path.join(BASE_DIR, "static")
templates_path = os.path.join(BASE_DIR, "templates")

app.mount("/static", StaticFiles(directory=static_path), name="static")
templates = Jinja2Templates(directory=templates_path)

config = pdfkit.configuration(wkhtmltopdf=r"C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")



# ✅ Your routes below
@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI!"}

@app.get("/search", response_class=HTMLResponse)
def search(request: Request, query: str):
    result = search_wikipedia(query)
    keywords = extract_keywords(result.get("Extract", ""))
    # For now, use placeholder insights
    strengths = "Strong brand in AI and large language models."
    weaknesses = "Limited diversification outside AI."
    differentiators = "Cutting-edge generative AI and big community adoption."
    action = "Highlight our broader product suite and security features."

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

    env = Environment(loader=FileSystemLoader("backend/templates"))
    template = env.get_template("battlecard.html")
    html_content = template.render(
        title=result.get("Title", ""),
        extract=result.get("Extract", ""),
        url=result.get("ContentURL", ""),
        keywords=keywords
    )

    pdf = pdfkit.from_string(html_content, False, configuration=config)

    return StreamingResponse(io.BytesIO(pdf), media_type="application/pdf", headers={
        "Content-Disposition": f"attachment; filename={query}_battlecard.pdf"
    })
