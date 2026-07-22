from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from .database import engine, Base
from .routes import tickets
import os
from pathlib import Path

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Support CRM System", version="1.0.0")

# Setup templates and static files
BASE_DIR = Path(__file__).resolve().parent.parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "frontend" / "templates"))
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "frontend" / "static")), name="static")

# Include routers
app.include_router(tickets.router)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/create", response_class=HTMLResponse)
async def create_ticket_page(request: Request):
    return templates.TemplateResponse("create.html", {"request": request})

@app.get("/ticket/{ticket_id}", response_class=HTMLResponse)
async def ticket_detail_page(request: Request, ticket_id: str):
    return templates.TemplateResponse("detail.html", {"request": request, "ticket_id": ticket_id})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)