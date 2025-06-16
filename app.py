import streamlit as st
import sounddevice as sd
import whisper
import os
from gtts import gTTS
import tempfile
import simpleaudio as sa
from pydub import AudioSegment
from scipy.io import wavfile
from openai import OpenAI
import numpy as np
import time
import shutil
import atexit
import warnings

warnings.filterwarnings('ignore', message='.*sample_rate will be ignored.*')

st.set_page_config(
    page_title="AI Voice Assistant",
    page_icon="🎙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'audio_files' not in st.session_state:
    st.session_state.audio_files = set()
if 'is_recording' not in st.session_state:
    st.session_state.is_recording = False
if 'input_method' not in st.session_state:
    st.session_state.input_method = "text"
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []  

AUDIO_DIR = "audio_files"
os.makedirs(AUDIO_DIR, exist_ok=True)

def cleanup_audio_files():
    """Clean up all audio files"""
    for file_path in st.session_state.audio_files:
        if os.path.exists(file_path):
            try:
                os.unlink(file_path)
            except Exception as e:
                print(f"Error cleaning up {file_path}: {e}")
    st.session_state.audio_files.clear()


atexit.register(cleanup_audio_files)

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

client = OpenAI(api_key=st.secrets["openai_api_key"])
model = whisper.load_model("base")

MEMORY_WINDOW_SIZE = 5  

def record_audio(duration=5):
    audio = sd.rec(int(duration * 16000), samplerate=16000, channels=1)
    sd.wait()
    return audio

def transcribe(audio):
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        filename = f.name
        wavfile.write(filename, 16000, audio)
    result = model.transcribe(filename)
    os.unlink(filename)
    return result["text"]

def get_conversation_context():
    """Get the last N turns of conversation for context"""
    if not st.session_state.conversation_history:
        return []
    
    recent_turns = st.session_state.conversation_history[-MEMORY_WINDOW_SIZE:]
    
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
        {"role": "system", "content": f"Personal Context: {PERSONAL_CONTEXT}"}
    ]
    
    messages.extend(conversation_context)
    
    messages.append({"role": "user", "content": user_input})
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        temperature=0.7
    )
    return response.choices[0].message.content

def mp3_to_wav(mp3_path, wav_path):
    sound = AudioSegment.from_mp3(mp3_path)
    sound.export(wav_path, format="wav")

def play_audio(file_path):
    wave_obj = sa.WaveObject.from_wave_file(file_path)
    play_obj = wave_obj.play()
    play_obj.wait_done()

def speak(text):
    try:
        tts = gTTS(text=text, lang='en', slow=False)
        mp3_path = None
        wav_path = None
        try:
            mp3_path = os.path.join(AUDIO_DIR, f"temp_{int(time.time())}_{np.random.randint(1000)}.mp3")
            wav_path = os.path.join(AUDIO_DIR, f"temp_{int(time.time())}_{np.random.randint(1000)}.wav")
            
            tts.save(mp3_path)
            sound = AudioSegment.from_mp3(mp3_path)
            sound = sound.speedup(playback_speed=1.2)
            sound.export(wav_path, format="wav")
            
            st.session_state.audio_files.add(wav_path)
            return wav_path
            
        finally:
            if mp3_path and os.path.exists(mp3_path):
                os.unlink(mp3_path)
    except Exception as e:
        st.error(f"Error in speech synthesis: {e}")
        return None

def process_user_input(user_input, input_type="text"):
    """Process user input and generate response"""
    if not user_input.strip():
        return
    
    user_message = {
        "role": "user", 
        "content": user_input,
        "input_type": input_type
    }
    st.session_state.messages.append(user_message)
    st.session_state.conversation_history.append({
        "role": "user",
        "content": user_input
    })
    
    with st.spinner("🤔 Processing your question..."):
        answer = chat_with_gpt(user_input)
        
        assistant_message = {
            "role": "assistant", 
            "content": answer
        }
        st.session_state.messages.append(assistant_message)
        st.session_state.conversation_history.append({
            "role": "assistant",
            "content": answer
        })
        
        with st.spinner("🔊 Converting response to speech..."):
            audio_path = speak(answer)
            if audio_path:
                st.session_state.messages[-1]["audio_path"] = audio_path
    st.rerun()

st.title("Chat with Yash")

col1, col2 = st.columns([2, 1])

with col1:
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if message["role"] == "user":
                input_type = message.get("input_type", "text")
                input_icon = "🎤" if input_type == "voice" else "✍️"
                st.markdown(f"**{input_icon} You ({input_type}):**")
            
            text_col, audio_col = st.columns([3, 1])
            
            with text_col:
                st.write(message["content"])
            
            if message.get("audio_path") and os.path.exists(message["audio_path"]):
                with audio_col:
                    with open(message["audio_path"], 'rb') as audio_file:
                        audio_bytes = audio_file.read()
                        st.audio(
                            audio_bytes,
                            format='audio/wav',
                            start_time=0,
                            autoplay=True
                        )

with col2:
    st.subheader("Input Method")
    input_method = st.radio(
        "Choose how to ask your question:",
        ["🎤 Voice Input", "✍️ Text Input"],
        key="input_method_radio",
        horizontal=True
    )
    
    st.session_state.input_method = "voice" if "Voice" in input_method else "text"
    
    if st.session_state.input_method == "text":
        st.subheader("✍️ Text Input")
        user_input = st.text_area(
            "Type your question here:",
            key="text_input",
            height=100,
            help="Type your question and press Enter or click Send"
        )
        if st.button("Send", key="send_text"):
            process_user_input(user_input, "text")
            
    else:
        st.subheader("🎤 Voice Input")
        st.markdown("Click the button below to start recording your question")
        
        if st.button("🎤 Record Question (6 seconds)", 
                     key="record_button",
                     help="Click and speak your question clearly"):
            with st.spinner("🎤 Recording... Speak now!"):
                audio = record_audio(duration=6)
                question = transcribe(audio)
                if question.strip():
                    process_user_input(question, "voice")
                else:
                    st.warning("No speech detected. Please try again.")

    st.markdown("---")
    st.subheader("Connect")
    
    st.markdown("""
    ### Yashaswa Varshney
    
    📧 **Email**: [yswa.var@icloud.com](mailto:yswa.var@icloud.com)  
    📱 **Phone**: [+91 6396300355](tel:+916396300355)  
    💼 **LinkedIn**: [linkedin.com/in/yashaswa-varshney](https://linkedin.com/in/yashaswa-varshney)  
    👨‍💻 **GitHub**: [github.com/yswa-var](https://github.com/yswa-var)  
    """)

    st.markdown("---")

if st.button("🗑️ Clear Chat", key="clear_chat"):
    st.session_state.messages = []
    st.session_state.conversation_history = []  
    st.rerun()