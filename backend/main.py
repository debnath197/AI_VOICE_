from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(title="Voice AI App")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))
FRONTEND_DIR = os.path.join(PROJECT_ROOT, "frontend")
INDEX_FILE = os.path.join(FRONTEND_DIR, "index.html")

if os.path.exists(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

@app.get("/")
def home():
    if os.path.exists(INDEX_FILE):
        return FileResponse(INDEX_FILE)
    return JSONResponse({"error": "index.html not found"}, status_code=404)

@app.get("/test")
def test():
    return {"status": "ok", "message": "Backend is working"}

@app.post("/ask")
async def ask_question(request: Request):
    data = await request.json()
    question = data.get("question", "").lower().strip()

    if "gis" in question:
        answer = "GIS stands for Geographic Information System. It is used to collect, manage, analyze, and visualize spatial data."
    elif "python" in question:
        answer = "Python is a programming language used for automation, scripting, web development, and data analysis."
    elif "arcgis" in question:
        answer = "ArcGIS is a GIS software used for mapping, spatial analysis, and geoprocessing."
    elif "network analysis" in question:
        answer = "Network analysis in GIS is used for routing, shortest path, service area, and closest facility analysis."
    elif "projection" in question:
        answer = "Projection is the method of converting the earth’s curved surface into a flat map."
    else:
        answer = f"You asked: {question}. This live demo is working, but for real AI answers on any topic, run the Ollama version locally."

    return {
        "question": question,
        "answer": answer
    }
