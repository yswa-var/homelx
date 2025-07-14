# Voice Chat with GPT Frontend

A React-based frontend for a voice-enabled chat application that integrates with OpenAI's GPT, Whisper, and TTS APIs.

## Features

- 🎙️ **Voice Recording**: Record audio using your microphone
- 🗣️ **Speech-to-Text**: Automatic transcription using OpenAI Whisper
- 💬 **AI Chat**: Conversational AI powered by GPT-4o
- 🔊 **Text-to-Speech**: Audio responses using OpenAI TTS
- 📱 **Responsive Design**: Works on desktop and mobile devices
- ⚡ **Real-time**: Live chat with typing indicators

## Components

### Recorder.jsx

- Uses `navigator.mediaDevices.getUserMedia()` for microphone access
- Records audio into a Blob
- POSTs audio to `/transcribe` endpoint
- Handles recording states and error handling

### Player.jsx

- Audio playback component using `URL.createObjectURL()`
- Auto-play functionality for TTS responses
- Play/pause controls with visual feedback

### App.jsx

- Main chat interface
- Manages conversation state and message history
- Integrates Recorder and Player components
- Handles API communication with backend

## Setup

1. Install dependencies:

   ```bash
   npm install
   ```

2. Start the development server:

   ```bash
   npm run dev
   ```

3. Make sure the backend is running on `http://localhost:8000`

## API Endpoints

The frontend communicates with these backend endpoints:

- `POST /transcribe` - Speech-to-text transcription
- `POST /chat` - GPT conversation
- `POST /tts` - Text-to-speech conversion

## Environment Variables

Make sure your backend has the following environment variable:

- `OPENAI_API_KEY` - Your OpenAI API key

## Usage

1. **Voice Chat**: Click "Start Recording" to speak, then "Stop Recording" to send
2. **Text Chat**: Type your message and press Enter or click Send
3. **Audio Response**: AI responses are automatically converted to speech and played

## Development

The app uses Vite for fast development with:

- Hot Module Replacement (HMR)
- Proxy configuration for API requests
- Modern React with hooks
- CSS modules for styling

## Browser Compatibility

- Modern browsers with Web Audio API support
- HTTPS required for microphone access in production
- Chrome, Firefox, Safari, Edge supported
