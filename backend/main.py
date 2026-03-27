from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(title="Live Voice Answer App")

# =========================
# CORS SETTINGS
# =========================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# PATH SETTINGS
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, ".."))
FRONTEND_DIR = os.path.join(PROJECT_ROOT, "frontend")
INDEX_FILE = os.path.join(FRONTEND_DIR, "index.html")

# =========================
# STATIC FILES (optional)
# =========================
if os.path.exists(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

# =========================
# HOME ROUTE -> LOAD FRONTEND
# =========================
@app.get("/")
def serve_frontend():
    if os.path.exists(INDEX_FILE):
        return FileResponse(INDEX_FILE)
    return JSONResponse(
        content={"error": "index.html not found in frontend folder"},
        status_code=404
    )

# =========================
# HEALTH CHECK ROUTE
# =========================
@app.get("/health")
def health_check():
    return {"message": "Voice Answer App Running"}

# =========================
# TEST ROUTE
# =========================
@app.get("/test")
def test():
    return {"status": "ok", "message": "Backend is working"}

# =========================
# SAMPLE ASK ROUTE (optional)
# =========================
@app.post("/ask")
async def ask_question():
    return {
        "answer": "Your backend is connected successfully!"
    }
