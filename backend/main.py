from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(title="Voice AI App")

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
    return {"status": "ok", "message": "Backend is working"}

# =========================
# ASK ROUTE
# =========================
@app.post("/ask")
async def ask_question(request: Request):
    data = await request.json()
    question = data.get("question", "").lower().strip()

    if not question:
        return {"answer": "Please ask a valid question."}

    if "gis" in question:
        answer = "GIS stands for Geographic Information System. It is used to collect, manage, analyze, and visualize spatial or location-based data."

    elif "remote sensing" in question:
        answer = "Remote sensing is the process of collecting information about the earth's surface without direct physical contact, usually through satellites, drones, or aerial imagery."

    elif "python" in question:
        answer = "Python is a powerful programming language used for automation, web development, scripting, data analysis, and GIS workflows."

    elif "arcgis" in question:
        answer = "ArcGIS is a GIS software platform used for mapping, spatial analysis, geoprocessing, and geographic data management."

    elif "qgis" in question:
        answer = "QGIS is an open-source GIS software used for map creation, spatial analysis, and geospatial data visualization."

    elif "network analysis" in question or "routing" in question or "shortest path" in question:
        answer = "Network analysis in GIS is used for routing, shortest path analysis, service area, and closest facility problems."

    elif "projection" in question or "coordinate system" in question:
        answer = "Projection is the method of converting the earth’s curved surface into a flat map. Coordinate systems help define accurate locations."

    elif "raster" in question:
        answer = "Raster data is made of pixels or cells and is used for continuous data like satellite imagery, temperature, and elevation."

    elif "vector" in question:
        answer = "Vector data represents geographic features using points, lines, and polygons such as cities, roads, and district boundaries."

    elif "topology" in question:
        answer = "Topology in GIS defines spatial relationships and rules such as no overlap, no gaps, and connectivity between features."

    elif "spatial join" in question:
        answer = "Spatial Join is a GIS operation used to combine attributes from one layer to another based on their spatial relationship."

    elif "geocoding" in question:
        answer = "Geocoding is the process of converting addresses or place names into geographic coordinates like latitude and longitude."

    elif "wms" in question:
        answer = "WMS stands for Web Map Service. It is used to serve map images over the internet."

    elif "wfs" in question:
        answer = "WFS stands for Web Feature Service. It is used to serve actual vector feature data over the internet."

    elif "hello" in question or "hi" in question:
        answer = "Hello! I am your voice AI assistant. Ask me anything."

    elif "interview" in question:
        answer = "For interview questions, answer clearly, confidently, and with real project examples whenever possible."

    else:
        answer = f"I understood your question: {question}. Right now this Render version supports many GIS and technical questions. For truly any-topic AI answers, connect Ollama locally or use an AI API."

    return {
        "question": question,
        "answer": answer
    }
