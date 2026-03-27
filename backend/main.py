from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(title="Live Voice Answer App")

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

# =========================
# STATIC FILES
# =========================
if os.path.exists(FRONTEND_DIR):
    app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

# =========================
# FRONTEND HOME
# =========================
@app.get("/")
def home():
    if os.path.exists(INDEX_FILE):
        return FileResponse(INDEX_FILE)
    return JSONResponse({"error": "index.html not found"}, status_code=404)

# =========================
# DEBUG ROUTES
# =========================
@app.get("/health")
def health():
    return {"message": "Voice Answer App Running"}

@app.get("/test")
def test():
    return {"status": "ok", "message": "Backend working"}

# =========================
# ASK ROUTE
# =========================
@app.post("/ask")
async def ask_question(request: Request):
    try:
        data = await request.json()
        question = data.get("question", "").strip()

        print("Received Question:", question)

        if not question:
            return {"answer": "No question received from frontend."}

        return {"answer": f"You said: {question}"}

    except Exception as e:
        print("ASK ERROR:", str(e))
        return JSONResponse(
            content={"answer": f"Backend error: {str(e)}"},
            status_code=500
        )
