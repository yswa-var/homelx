import openai
import sounddevice as sd
import whisper
import os
from gtts import gTTS
import tempfile
import simpleaudio as sa
from pydub import AudioSegment
from scipy.io import wavfile
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SYSTEM_PROMPT = "You are a helpful AI assistant. Provide clear, concise, and accurate responses."

# Get API key from environment variable
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set")

openai.api_key = api_key
model = whisper.load_model("base")

client = OpenAI(api_key=api_key)

def record_audio(duration=5):
    print("Recording...")
    audio = sd.rec(int(duration * 16000), samplerate=16000, channels=1)
    sd.wait()
    return audio

def transcribe(audio):
    # Save and transcribe
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
        filename = f.name
        wavfile.write(filename, 16000, audio)
    result = model.transcribe(filename)
    os.unlink(filename)  # Clean up the temporary file
    return result["text"]

def chat_with_gpt(user_input):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_input}
        ]
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
        tts = gTTS(text)
        mp3_path = None
        wav_path = None
        try:
            # Create temporary files
            mp3_file = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False)
            mp3_path = mp3_file.name
            mp3_file.close()
            
            wav_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
            wav_path = wav_file.name
            wav_file.close()
            
            # Save and convert
            tts.save(mp3_path)
            mp3_to_wav(mp3_path, wav_path)
            
            # Play audio
            play_audio(wav_path)
            
        finally:
            # Cleanup
            if mp3_path and os.path.exists(mp3_path):
                os.unlink(mp3_path)
            if wav_path and os.path.exists(wav_path):
                os.unlink(wav_path)
    except Exception as e:
        print(f"Error in speech synthesis: {e}")

def main():
    while True:
        print("\nSpeak your question (Ctrl+C to exit):")
        audio = record_audio(duration=6)
        question = transcribe(audio)
        print(f"You asked: {question}")
        answer = chat_with_gpt(question)
        print(f"Bot: {answer}")
        speak(answer)

if __name__ == "__main__":
    main()
