import streamlit as st
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase, WebRtcMode
import whisper
import numpy as np
import av
import tempfile
import soundfile as sf

# Load Whisper model once
model = whisper.load_model("base")

class AudioProcessor(AudioProcessorBase):
    def __init__(self) -> None:
        self.audio_buffer = []

    def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
        audio = frame.to_ndarray()
        self.audio_buffer.append(audio)
        return frame

    def get_audio_data(self):
        if not self.audio_buffer:
            return None
        return np.concatenate(self.audio_buffer, axis=1).flatten()

st.title("🎙️ Streamlit Audio to Text")

# Setup WebRTC streamer (audio only)
ctx = webrtc_streamer(
    key="audio-transcriber",
    mode=WebRtcMode.SENDONLY,
    audio_processor_factory=AudioProcessor,
    media_stream_constraints={"video": False, "audio": True},
)

# Transcription logic
if ctx.audio_processor:
    if st.button("Transcribe"):
        audio_data = ctx.audio_processor.get_audio_data()
        if audio_data is not None:
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
                sf.write(f.name, audio_data, samplerate=48000, format='WAV')
                st.info("Transcribing...")
                result = model.transcribe(f.name)
                st.success("Transcription Result:")
                st.write(result["text"])
        else:
            st.warning("No audio data captured.")
