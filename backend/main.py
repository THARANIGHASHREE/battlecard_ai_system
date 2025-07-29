from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, StreamingResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from backend.data_collection import search_wikipedia
from backend.text_analysis import extract_keywords
from backend.database import Battlecard, save_battlecard, create_db, get_all_battlecards
from backend.auth import create_user, authenticate_user, get_current_user, User

import pdfkit
import io
import os
from jinja2 import Environment, FileSystemLoader

app = FastAPI()

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
static_path = os.path.join(BASE_DIR, "static")
templates_path = os.path.join(BASE_DIR, "templates")

app.mount("/static", StaticFiles(directory=static_path), name="static")
templates = Jinja2Templates(directory=templates_path)

# PDF Configuration
config = pdfkit.configuration(wkhtmltopdf=r"C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe")

# Database Initialization
create_db()

# Home Route
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

# Signup Routes
@app.get("/signup", response_class=HTMLResponse)
def signup_form(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.post("/signup", response_class=HTMLResponse)
def signup_submit(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):
    try:
        create_user(username=username, email=email, password=password)
        return RedirectResponse(url="/login", status_code=303)
    except Exception as e:
        return templates.TemplateResponse("signup.html", {"request": request, "error": str(e)})

# Login Routes
@app.get("/login", response_class=HTMLResponse)
def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login", response_class=HTMLResponse)
def login_submit(request: Request, username: str = Form(...), password: str = Form(...)):
    token = authenticate_user(username, password)
    if not token:
        return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})
    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie(key="token", value=token, httponly=True)
    return response

@app.get("/logout")
def logout():
    response = RedirectResponse(url="/")
    response.delete_cookie("token")
    return response

# Battlecard Generator
@app.get("/search", response_class=HTMLResponse)
def search(request: Request, query: str, user: User = Depends(get_current_user)):
    result = search_wikipedia(query)
    keywords = extract_keywords(result.get("Extract", ""))

    strengths = "Strong ecosystem."
    weaknesses = "Legacy systems."
    differentiators = "Cloud + Office combo."
    action = "Offer faster integration & trials."

    card = Battlecard(
        username=user.username,
        company=query,
        extract=result.get("Extract", ""),
        keywords=", ".join(keywords),
        strengths=strengths,
        weaknesses=weaknesses,
        differentiators=differentiators,
        action=action
    )
    save_battlecard(card)

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

# PDF Download
@app.get("/download", response_class=StreamingResponse)
def download(query: str, user: User = Depends(get_current_user)):
    result = search_wikipedia(query)
    keywords = extract_keywords(result.get("Extract", ""))

    strengths = "Strong ecosystem."
    weaknesses = "Legacy systems."
    differentiators = "Cloud + Office combo."
    action = "Offer faster integration & trials."

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

# History Page
@app.get("/history", response_class=HTMLResponse)
def history(request: Request, user: User = Depends(get_current_user)):
    all_cards = get_all_battlecards()
    user_cards = [c for c in all_cards if c.username == user.username]
    return templates.TemplateResponse("history.html", {
        "request": request,
        "battlecards": user_cards
    })
