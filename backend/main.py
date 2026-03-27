from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from answer_service import generate_answer, transcribe_audio
import shutil
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = "temp_audio"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/")
def home():
    return {"message": "Voice Answer App Running"}

@app.post("/process-audio")
async def process_audio(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    transcript = transcribe_audio(file_path)
    answer = generate_answer(transcript)

    return {
        "transcript": transcript,
        "answer": answer
    }
