import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def transcribe_audio(file_path):
    with open(file_path, "rb") as audio_file:
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    return transcript.text

def generate_answer(question):
    prompt = f"""
You are an interview preparation assistant.
The user is practicing and wants a professional, concise spoken answer.

Question:
{question}

Return:
1. Short answer (2-3 lines)
2. Interview-ready answer (spoken style)
3. 3 important points to mention

Do not fabricate personal experience.
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are a professional interview coach."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.6
    )

    return response.choices[0].message.content
