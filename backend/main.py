import os
import json
from typing import Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY not found in environment variables")

app = FastAPI()

# Yash's personal system prompt and context
SYSTEM_PROMPT = """
# Yashaswa Varshney (YASH)
Email:yswa.var@icloud.com Phone: +91 6396300355 GitHub: github.com/yswa-var
# Role: AI Application Developer;
software developer currently working at HyperBots.
# work experience
* Software Development Engineer at HyperBots
* Software Development Engineer at Finzome 
# Core Expertise
* Multi-Agent Orchestration: Designed LocoForge with LangGraph/MCP for robust SQL/NoSQL query execution.
* Speech & Chat AI: Integrated Whisper-1, GPT-4o, and TTS-1 for seamless voice interaction.
* Full-Stack Delivery: Built REST endpoints and a responsive React UI with real-time WebSocket/SSE.
* DevOps Automation: Dockerized services, implemented CI/CD with GitHub Actions, and managed vector DB retrieval.
# Key Projects
* Tilt-Valid: MPC-Based Distributed Validator System for Solana
* LocoForge: Natural-language query orchestrator for SQL/NoSQL with planner/executor nodes.
* EasyBt: Python library for rapid financial strategy backtesting.
* Pocket++: CLI tool for article summarization via NLP and automation.
# Skills & Education
* Languages: Python, TypeScript, SQL, Bash
* Tools: FastAPI, React, Tailwind, LangGraph, OpenAI SDK, Docker
* AI: Whisper-1, GPT-4o, TTS-1, RAG, vector DBs
* DevOps: GitHub Actions, AWS/GCP, WebSockets
B.Tech, Computer Science (KIIT University, CGPA 8.30; Minor: Financial Economics)
# Ethos
Agile problem-solver, collaborative communicator, lifelong learner passionate about AI and software development.
always reply in humanly way and be friendly aslways repling like a human. always reply in ENGLISH only

"""

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

# Pydantic models for request/response
class ChatRequest(BaseModel):
    message: str
    conversationId: Optional[str] = None

class ChatResponse(BaseModel):
    reply: str
    conversationId: str

class TTSRequest(BaseModel):
    text: str

@app.get("/")
def root():
    return {"message": "Chat with Yashaswa backend is running"}

@app.post("/transcribe")
async def transcribe_audio(audio_file: UploadFile = File(...)):
    """
    Accepts audio blob and transcribes it using Whisper
    """
    try:
        # Read the audio file
        audio_content = await audio_file.read()
        
        # Create a file-like object with the proper filename
        import io
        file_obj = io.BytesIO(audio_content)
        file_obj.name = audio_file.filename or "audio.mp3"
        
        # Call OpenAI Whisper API using new syntax
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=file_obj
        )
        
        return {"text": response.text}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")

@app.post("/chat", response_model=ChatResponse)
async def chat_with_gpt(request: ChatRequest):
    """
    Accepts message and conversationId, calls GPT-4o/turbo, returns reply + updated conversationId
    """
    try:
        # Prepare messages for the conversation
        messages = []
        
        # Add Yash's personalized system message
        messages.append({
            "role": "system", 
            "content": SYSTEM_PROMPT
        })
        
        # If conversationId is provided, you might want to retrieve previous messages
        # For now, we'll start fresh each time
        if request.conversationId:
            # In a real implementation, you'd retrieve conversation history from a database
            pass
        
        messages.append({"role": "user", "content": request.message})
        
        # Call OpenAI GPT-4o API using new syntax
        response = client.chat.completions.create(
            model="gpt-4o",  # or "gpt-4o-mini" for faster/cheaper responses
            messages=messages,
            max_tokens=1000,
            temperature=0.7
        )
        
        reply = response.choices[0].message.content
        
        # Generate a new conversationId (in a real app, you'd store this in a database)
        import uuid
        new_conversation_id = str(uuid.uuid4())
        
        return ChatResponse(
            reply=reply,
            conversationId=new_conversation_id
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")

@app.post("/tts")
async def text_to_speech(request: TTSRequest):
    """
    Accepts text and returns audio using TTS-1 API
    """
    try:
        # Call OpenAI TTS-1 API using new syntax
        response = client.audio.speech.create(
            model="tts-1",
            voice="fable",  # Options: alloy, echo, fable, onyx, nova, shimmer
            input=request.text
        )
        
        # Get the audio content
        audio_content = response.content
        
        # Return the audio as a streaming response
        return StreamingResponse(
            iter([audio_content]),
            media_type="audio/mpeg",
            headers={"Content-Disposition": "attachment; filename=speech.mp3"}
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS failed: {str(e)}")
