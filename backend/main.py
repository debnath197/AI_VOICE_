from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from openai import OpenAI
import os

app = FastAPI(title="Live Voice Answer App")

# =========================
# OPENAI SETUP
# =========================
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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
# HOME ROUTE
# =========================
@app.get("/")
def home():
    if os.path.exists(INDEX_FILE):
        return FileResponse(INDEX_FILE)
    return JSONResponse(
        content={"error": "index.html not found in frontend folder"},
        status_code=404
    )

# =========================
# HEALTH
# =========================
@app.get("/health")
def health():
    return {"message": "Voice Answer App Running"}

# =========================
# TEST
# =========================
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
            return {"answer": "I could not hear your question properly. Please try again."}

        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful AI voice assistant. Answer clearly, shortly, and naturally so it sounds good when spoken aloud."
                },
                {
                    "role": "user",
                    "content": question
                }
            ],
            temperature=0.7,
            max_tokens=200
        )

        answer = response.choices[0].message.content.strip()

        return {"answer": answer}

    except Exception as e:
        print("ASK ERROR:", str(e))
        return JSONResponse(
            content={"answer": f"Backend error: {str(e)}"},
            status_code=500
        )
