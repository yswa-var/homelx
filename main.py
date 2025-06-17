from fastapi import FastAPI, UploadFile, File, Form, BackgroundTasks, HTTPException, APIRouter
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
import shutil
import tempfile
import numpy as np
import time
import wave
from dotenv import load_dotenv
import whisper
from openai import OpenAI
from gtts import gTTS
from pydub import AudioSegment
from scipy.io import wavfile
import atexit
import uuid

# Load environment variables
load_dotenv()

# FastAPI app
app = FastAPI()

# Allow CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"]
)

AUDIO_DIR = "audio_files"
os.makedirs(AUDIO_DIR, exist_ok=True)

SYSTEM_PROMPT = """# Yashaswa Varshney (YASH)
**Email**: yswa.var@icloud.com  
**Phone**: +91 6396300355  
**LinkedIn**: [linkedin.com/in/yashaswa-varshney](https://linkedin.com/in/yashaswa-varshney)  
**GitHub**: [github.com/yswa-var](https://github.com/yswa-var)  
## Experience
### HyperBots, Bengaluru, IN  
**Software Development Engineer**  
*Aug 2024 – Present*  
- Developed ERP connectors for AI-driven accounts payable workflows, improving data exchange.  
- Implemented real-time notifications (email, WhatsApp, web), reducing turnaround time.  
### Finzome, Mumbai, IN  
**Software Developer Intern**  
*Jun 2024 – Aug 2024*  
- Built a backtesting framework for stocks; reduced runtime using Cython.  
- Optimized trading strategies via parameter tuning.  
- Designed backend and integrated payments for LMS (90%+ success rate).  
### AR Quants, Mumbai, IN  
**Software Developer Intern**  
*Feb 2023 – Aug 2023*  
- Built statistical tools for transaction analysis.  
- Designed InfluxDB-based timeseriesDB storage.  
- Created custom Pine Script indicators for market pattern visualization.  
## Projects
### [Multi-Database Query Orchestrator](https://github.com/yswa-var/LocoForge)  
*LangGraph, MCP, SQL, MongoDB*  
- Unified natural language interface for SQL, NoSQL, and Drive-based queries.  
- Features layered agent system: Planner, Executor, and Error Handler.  
- Supports schema-aware, context-sensitive query generation.  
*  [**EasyBt**](https://github.com/yswa-var/EasyBt): Python library to backtest trading strategies and generate alpha signals effortlessly.
*  [**Pocket++**](https://github.com/yswa-var/pocketpp): Terminal tool to summarize and save long web articles for fast reading and recall.
*  [**FilthyFilter**](https://github.com/yswa-var/FilthyFilter): Extracts high-quality anime wallpapers by filtering scenes using computer vision and OCR.
*  [**RRG**](https://github.com/yswa-var/RRG): Bloomberg-style Sector Rotation Graph to visualize market swings using Streamlit and Yahoo Finance data.
*  [**Chartink-Backtestor**](https://github.com/yswa-var/chartink-backtestor): Analyze and backtest sectoral scans from Chartink with performance tracking.
## Technical Skills
- **Tools & Frameworks**: REST API, PyTorch, LangGraph, LangChain, RAG, Vector DBs, MCP  
- **Platforms**: Pine Script, GitHub, DB Ops, AWS  
- **Languages**: Python, Golang (learning), SQL, Bash  
- **Domains**: AI Agents, Financial Systems, Automation  
- **Soft Skills**: Analytical Thinking, Design Thinking, Planning  
## Education
**KIIT University, Bhubaneswar, IN**  
*School of Computer Science*  
**B.Tech in Computer Science Engineering**  
*Sep 2020 – Sep 2024*  
- **CGPA**: 8.30  
- **Coursework**: Financial Economics using Data Analytics  
## Achievements
- Contributed to Flowise Python connectors (AI agent infra).  
- Blog: "[Nadaraya-Watson Indicator](https://medium.com/@yashaswa/backtesting-the-viral-nadaraya-watson-envelop-trading-indicator-in-python-b800a70e8167)" [12.5K+ views].  
- Speaker: UN Workshop on Power BI.  
- ArtStation: *Utopia Concept Art Winner*, Spring 2020.  
## Interests
- Blogging 
- Himalayan trekking
- Swimming  
- Hiking  .
Key aspects of your personality and experience:
- You're analytical and detail-oriented, with strong problem-solving skills
- You have experience in building AI-driven systems and financial tools
- You've worked on projects like Multi-Database Query Orchestrator and Sector Rotation Graph
- You're interested in blogging about finance and AI, and enjoy outdoor activities like trekking
- You have a background in both technical and financial domains
- You save time by replying in a concise manner
When responding to questions:
1. Be authentic and personal, drawing from your actual experiences
2. Maintain a professional yet approachable tone
3. Use specific examples from your work and projects
4. Be honest about your strengths and areas for growth
5. Share your genuine interests and passions

Remember: You are Yashaswa Varshney, and you should respond as if you are speaking directly to the person asking the question."""

PERSONAL_CONTEXT = {
    "name": "Yashaswa Varshney you can call me Yash",
    "current_role": "Software Development Engineer at HyperBots",
    "education": "B.Tech in Computer Science from KIIT University 2024 Graduate",
    "skills": ["AI Agents", "Financial Systems", "Automation", "Python", "LangGraph", "RAG"],
    "projects": [
        "Multi-Database Query Orchestrator",
        "Sector Rotation Graph",
        "FilthyFilter"
    ],
    "interests": ["Blogging (Finance, AI)", "Himalayan trekking", "Swimming", "Hiking"],
    "achievements": [
        "Contributed to Flowise Python connectors",
        "Blog on Nadaraya-Watson Indicator with 12.5K+ views",
        "Speaker at UN Workshop on Power BI",
        "ArtStation Utopia Concept Art Winner"
    ]
}

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
model = whisper.load_model("base")
MEMORY_WINDOW_SIZE = 5

# In-memory chat history (for demo; use persistent store for production)
conversation_history = []

def get_conversation_context():
    if not conversation_history:
        return []
    recent_turns = conversation_history[-MEMORY_WINDOW_SIZE:]
    formatted_context = []
    for turn in recent_turns:
        formatted_context.append({
            "role": turn["role"],
            "content": turn["content"]
        })
    return formatted_context

def chat_with_gpt(user_input):
    conversation_context = get_conversation_context()
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
    ]
    messages.extend(conversation_context)
    messages.append({"role": "user", "content": user_input})
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0.7
    )
    return response.choices[0].message.content

def speak(text):
    try:
        tts = gTTS(text=text, lang='en', slow=False)
        mp3_path = os.path.join(AUDIO_DIR, f"temp_{uuid.uuid4().hex}.mp3")
        wav_path = os.path.join(AUDIO_DIR, f"temp_{uuid.uuid4().hex}.wav")
        tts.save(mp3_path)
        sound = AudioSegment.from_mp3(mp3_path)
        sound = sound.speedup(playback_speed=1.2)
        sound.export(wav_path, format="wav")
        os.unlink(mp3_path)
        return wav_path
    except Exception as e:
        print(f"Error in speech synthesis: {e}")
        return None

def transcribe_audio_file(audio_path):
    result = model.transcribe(audio_path)
    return result["text"]

def cleanup_audio_files():
    for fname in os.listdir(AUDIO_DIR):
        try:
            os.unlink(os.path.join(AUDIO_DIR, fname))
        except Exception as e:
            print(f"Error cleaning up {fname}: {e}")

atexit.register(cleanup_audio_files)

class ChatRequest(BaseModel):
    user_input: str
    input_type: str = "text"  # "text" or "voice"

class ChatResponse(BaseModel):
    question: str
    answer: str
    audio_url: str = None

# --- API ROUTER ---
api_router = APIRouter()

@api_router.post("/chat", response_model=ChatResponse)
def chat_endpoint(request: ChatRequest, background_tasks: BackgroundTasks):
    user_input = request.user_input
    input_type = request.input_type
    if not user_input.strip():
        raise HTTPException(status_code=400, detail="Empty input")
    conversation_history.append({"role": "user", "content": user_input})
    answer = chat_with_gpt(user_input)
    conversation_history.append({"role": "assistant", "content": answer})
    audio_path = speak(answer)
    audio_url = None
    if audio_path:
        audio_url = f"/api/audio/{os.path.basename(audio_path)}"
    # Removed immediate cleanup to allow frontend to access audio files
    return ChatResponse(question=user_input, answer=answer, audio_url=audio_url)

@api_router.post("/voice", response_model=ChatResponse)
def voice_chat_endpoint(background_tasks: BackgroundTasks, file: UploadFile = File(...)):
    suffix = os.path.splitext(file.filename)[-1]
    temp_path = os.path.join(AUDIO_DIR, f"input_{uuid.uuid4().hex}{suffix}")
    with open(temp_path, "wb") as f:
        shutil.copyfileobj(file.file, f)
    question = transcribe_audio_file(temp_path)
    print(f"Question: {question}")
    os.unlink(temp_path)
    if not question.strip():
        raise HTTPException(status_code=400, detail="No speech detected")
    conversation_history.append({"role": "user", "content": question})
    answer = chat_with_gpt(question)
    conversation_history.append({"role": "assistant", "content": answer})
    audio_path = speak(answer)
    audio_url = None
    if audio_path:
        audio_url = f"/api/audio/{os.path.basename(audio_path)}"
    return ChatResponse(question=question, answer=answer, audio_url=audio_url)

@api_router.get("/audio/{filename}")
def get_audio(filename: str):
    file_path = os.path.join(AUDIO_DIR, filename)
    print(f"File path: {file_path}")
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Audio not found")
    return FileResponse(file_path, media_type="audio/wav")

@api_router.post("/clear")
def clear_chat():
    conversation_history.clear()
    cleanup_audio_files()
    return {"status": "cleared"}

@api_router.get("/user_info")
def get_user_info():
    return PERSONAL_CONTEXT

@api_router.post("/delete_audio_files")
def delete_audio_files():
    try:
        print("Deleting audio files...")
        cleanup_audio_files()
        print("Audio files deleted successfully")
        return {"status": "success", "message": "audio files deleted"}
    except Exception as e:
        print(f"Error deleting audio files: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to delete audio files: {str(e)}")

@api_router.get("/test")
def test_endpoint():
    return {"status": "success", "message": "API is working"}

# Register the API router with prefix /api
app.include_router(api_router, prefix="/api")

# Serve React static files (MUST be last)
app.mount("/", StaticFiles(directory="frontend/build", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
