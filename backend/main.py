from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(title="Free Voice Answer App")

# =========================
# CORS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# PATHS
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))
FRONTEND_DIR = os.path.join(PROJECT_ROOT, "frontend")
INDEX_FILE = os.path.join(FRONTEND_DIR, "index.html")

if os.path.exists(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

# =========================
# HOME
# =========================
@app.get("/")
def home():
    if os.path.exists(INDEX_FILE):
        return FileResponse(INDEX_FILE)
    return JSONResponse({"error": "index.html not found"}, status_code=404)

# =========================
# TEST
# =========================
@app.get("/test")
def test():
    return {"status": "ok"}

# =========================
# ASK ROUTE (FREE AI)
# =========================
@app.post("/ask")
async def ask_question(request: Request):
    data = await request.json()
    question = data.get("question", "").lower()

    print("Question:", question)

    # 🔥 FREE SMART ANSWERS
    if "gis" in question:
        return {"answer": "GIS stands for Geographic Information System. It is used to collect, manage, analyze, and visualize spatial data."}

    elif "python" in question:
        return {"answer": "Python is a programming language widely used for automation, data analysis, and GIS scripting."}

    elif "arcgis" in question:
        return {"answer": "ArcGIS is a GIS software used for mapping, spatial analysis, and geoprocessing."}

    elif "network analysis" in question:
        return {"answer": "Network analysis in GIS is used to find shortest path, routing, and service areas."}

    elif "projection" in question:
        return {"answer": "Projection converts the earth's curved surface into a flat map."}

    elif "hello" in question or "hi" in question:
        return {"answer": "Hello! How can I help you today?"}

    elif "interview" in question:
        return {"answer": "In GIS interviews, focus on spatial analysis, projections, Python, and real project experience."}

    else:
        return {"answer": "I am a free AI assistant. Please ask about GIS, Python, or interview topics."}
