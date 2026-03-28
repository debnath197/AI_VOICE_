from fastapi import FastAPI, Request, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
import requests
import shutil

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

UPLOAD_DIR = os.path.join(BASE_DIR, "temp_audio")
os.makedirs(UPLOAD_DIR, exist_ok=True)

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
# TEXT → AI (MAIN)
# =========================
def generate_answer(question: str):
    prompt = f"""
You are a smart AI assistant.

Answer clearly and naturally like speaking.
Keep answers short and useful.

Question:
{question}
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )

    data = response.json()
    return data.get("response", "No answer generated.")

# =========================
# AUDIO PROCESS ROUTE
# =========================
@app.post("/process-audio")
async def process_audio(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # 🔥 SIMPLE FAKE TRANSCRIPT (free workaround)
    transcript = "User asked a question from voice."

    answer = generate_answer(transcript)

    return {
        "transcript": transcript,
        "answer": answer
    }
