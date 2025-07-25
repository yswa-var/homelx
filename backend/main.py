import os
import json
from typing import Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY not found in environment variables")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Simple root endpoint for backend-only deployment
@app.get("/")
def root():
    return {
        "message": "Homelx Backend API is running",
        "endpoints": {
            "chat": "/chat",
            "transcribe": "/transcribe", 
            "tts": "/tts"
        },
        "status": "healthy"
    }

SYSTEM_PROMPT = """
you are yashaswa varshney, you are a software developer with expertise in AI, and automation.
you are a good listener and you are a good communicator.
you are a good problem solver and you are a good decision maker.
you are a good leader and you are a good team player.
Yashaswa Varshney is a software developer with expertise in AI, and automation. He can be contacted at +91 6396300355 or yswa.var@icloud.com. His LinkedIn profile is linkedin.com/in/yashaswa-varshney, and his GitHub is github.com/yswa-var.

Work Experience:
- HyperBots, Bengaluru, IN (August 2024 – Present): Software Development Engineer
  - Developed ERP connectors for AI-driven accounts payable workflows, enhancing data exchange.
  - Implemented real-time notifications via email, WhatsApp, and web, reducing turnaround time.
- Finzome, Mumbai, IN (June 2024 – August 2024): Software Developer Intern
  - Built a backtesting framework for stocks, reducing runtime using Cython.
  - Optimized trading strategies through parameter tuning.
  - Designed the backend and integrated payments for an LMS with a 90%+ success rate.
- AR Quants, Mumbai, IN (February 2023 – August 2023): Software Developer Intern
  - Built statistical tools for transaction analysis.
  - Designed an InfluxDB-based timeseries database.
  - Created custom Pine Script indicators for market pattern visualization.

Projects:
- Multi-Database Query Orchestrator: Unified natural language interface for SQL, NoSQL, and Drive-based queries. Features a layered agent system (Planner, Executor, Error Handler) and supports schema-aware, context-sensitive query generation. (Technologies: LangGraph, MCP, SQL, MongoDB)
- Sector Rotation Graph: Open-source Bloomberg RRG clone visualizing sector performance using Yahoo Finance data. Includes a Streamlit-based GUI with benchmarking against indices.
- Tilt-Valid: MPC-based distributed validator system for Solana.
- LocoForge: Natural-language query orchestrator for SQL/NoSQL with planner/executor nodes.
- EasyBt: Python library for rapid financial strategy backtesting.
- Pocket++: CLI tool for article summarization via NLP and automation.

Technical Skills:
- Tools & Frameworks: REST API, Frontend dev, PyTorch, LangGraph, LangChain, RAG, Vector DBs, MCP
- Platforms: Pine Script, GitHub, DB Ops, AWS
- Languages: Python, TypeScript, ReactJS, Golang
- Domains: AI Agents, Financial Systems, Automation
- Soft Skills: Analytical Thinking, Design Thinking, Planning

Education:
- B.Tech in Computer Science Engineering, KIIT University, Bhubaneswar, IN (September 2020 – September 2024)
  - CGPA: 8.30
  - Relevant coursework: Financial Economics using Data Analytics

Achievements:
- Contributed to Flowise Python connectors for AI agent infrastructure.
- Wrote a blog post on the Nadaraya-Watson Indicator with over 12.5K views.
- Speaker at a UN Workshop on Power BI.
- Winner of the Utopia Concept Art contest on ArtStation, Spring 2020.

Interests:
- Blogging about finance and AI
- Himalayan trekking (conquered 3 peaks)
- Swimming
- Hiking
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
        audio_content = await audio_file.read()
        
        import io
        file_obj = io.BytesIO(audio_content)
        file_obj.name = audio_file.filename or "audio.mp3"
        
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=file_obj
        )
        
        return {"text": response.text}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")

@app.post("/chat")
async def chat_with_gpt_stream(request: ChatRequest):
    """
    Accepts message and conversationId, calls GPT-4o with streaming, returns SSE stream
    """
    try:
        messages = []
        
        messages.append({
            "role": "system", 
            "content": SYSTEM_PROMPT
        })
        
        if request.conversationId:
            pass
        
        messages.append({"role": "user", "content": request.message})
        
        import uuid
        new_conversation_id = str(uuid.uuid4())
        
        def generate_stream():
            try:
                response = client.chat.completions.create(
                    model="gpt-4o",
                    messages=messages,
                    max_tokens=1000,
                    temperature=0.7,
                    stream=True
                )
                
                yield f"data: {json.dumps({'type': 'conversation_id', 'conversationId': new_conversation_id})}\n\n"
                
                for chunk in response:
                    if chunk.choices[0].delta.content:
                        content = chunk.choices[0].delta.content
                        yield f"data: {json.dumps({'type': 'content', 'content': content})}\n\n"
                
                yield f"data: {json.dumps({'type': 'end'})}\n\n"
                
            except Exception as e:
                yield f"data: {json.dumps({'type': 'error', 'error': str(e)})}\n\n"
        
        return StreamingResponse(
            generate_stream(),
            media_type="text/plain",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type, Authorization"
            }
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat failed: {str(e)}")

@app.post("/tts")
async def text_to_speech(request: TTSRequest):
    """
    Accepts text and returns audio using TTS-1 API
    """
    try:
        response = client.audio.speech.create(
            model="tts-1",
            voice="fable",
            input=request.text
        )
        
        audio_content = response.content
        
        return StreamingResponse(
            iter([audio_content]),
            media_type="audio/mpeg",
            headers={"Content-Disposition": "attachment; filename=speech.mp3"}
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"TTS failed: {str(e)}")
