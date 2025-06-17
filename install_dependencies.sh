#!/bin/bash

# Install dependencies with fallback for openai-whisper
echo "Installing Python dependencies..."

# First, try to install everything except openai-whisper
pip install setuptools>=65.0.0 wheel>=0.38.0 pip>=23.0.0 build>=0.10.0
pip install streamlit>=1.24.0 sounddevice>=0.4.6 gTTS>=2.3.2 pydub>=0.25.1
pip install scipy>=1.11.3 openai>=1.3.0 numpy>=1.24.0 PyAudio>=0.2.13
pip install watchdog>=3.0.0 python-dotenv fastapi python-multipart uvicorn

# Try different approaches for openai-whisper
echo "Installing openai-whisper..."
if pip install openai-whisper==20231117; then
    echo "Successfully installed openai-whisper==20231117"
elif pip install openai-whisper==20230918; then
    echo "Successfully installed openai-whisper==20230918"
elif pip install openai-whisper; then
    echo "Successfully installed latest openai-whisper"
else
    echo "Failed to install openai-whisper, trying alternative method..."
    pip install --no-deps openai-whisper==20231117
    pip install torch torchaudio
fi

echo "Dependency installation completed!" 