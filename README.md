# HomeLX - Voice Chat with Streaming GPT

A real-time voice chat application with streaming GPT responses and markdown rendering.

## Features

- 🎙️ **Voice-to-Text**: Record voice messages using Whisper API
- 💬 **Streaming Chat**: Real-time GPT responses with streaming API
- 📝 **Markdown Rendering**: Beautiful markdown formatting for assistant responses
- 🔊 **Text-to-Speech**: Audio playback of responses using OpenAI TTS
- 🎨 **Modern UI**: Clean, responsive interface

## Recent Updates

### Streaming GPT Responses

- Backend now uses OpenAI's streaming API (`stream=True`)
- Server-Sent Events (SSE) for real-time response streaming
- Frontend handles streaming responses with live updates
- Animated streaming indicator shows when GPT is generating text

### Markdown Rendering

- Assistant responses are rendered as markdown using `react-markdown`
- Supports code blocks, headers, lists, links, and more
- Styled code highlighting and formatting
- Maintains conversation formatting while improving readability

## Tech Stack

### Backend

- **FastAPI** - API framework
- **OpenAI API** - GPT-4o, Whisper, TTS
- **Server-Sent Events** - For streaming responses
- **Python 3.12+**

### Frontend

- **React** - UI framework
- **Vite** - Build tool
- **react-markdown** - Markdown rendering
- **Modern CSS** - Styling and animations

## Getting Started

### Prerequisites

- Python 3.12+
- Node.js 18+
- OpenAI API key

### Installation

1. Clone the repository
2. Install backend dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Install frontend dependencies:

   ```bash
   cd frontend
   npm install
   ```

4. Set up environment variables:
   ```bash
   # Create .env file in backend directory
   OPENAI_API_KEY=your_openai_api_key_here
   ```

### Running the Application

1. Start the backend server:

   ```bash
   cd backend
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

2. Start the frontend development server:

   ```bash
   cd frontend
   npm run dev
   ```

3. Open http://localhost:5173 in your browser

## Usage

1. **Voice Input**: Click the microphone button to record voice messages
2. **Text Input**: Type messages in the text input field
3. **Streaming Responses**: Watch as GPT responses stream in real-time
4. **Markdown Formatting**: Assistant responses support markdown formatting
5. **Audio Playback**: Listen to TTS audio responses

## API Endpoints

- `POST /transcribe` - Convert audio to text using Whisper
- `POST /chat` - Stream GPT responses using SSE
- `POST /tts` - Convert text to speech using OpenAI TTS

## Architecture

The application uses a streaming architecture:

1. Frontend sends request to `/chat` endpoint
2. Backend creates OpenAI streaming response
3. Server-Sent Events stream response chunks to frontend
4. Frontend renders markdown and updates UI in real-time
5. TTS conversion happens after streaming completes

## Deployment

### Render Deployment

This application is configured for deployment on Render as a monorepo. See [DEPLOYMENT.md](./DEPLOYMENT.md) for detailed deployment instructions.

### Quick Deploy

1. Push your code to a Git repository
2. Connect your repository to Render
3. Set the `OPENAI_API_KEY` environment variable
4. Deploy using the `render.yaml` configuration

### Local Development

Use the provided development script:

```bash
./dev.sh
```

This will start both frontend and backend servers automatically.

## Contributing

This is a personal project showcasing modern AI chat implementation with streaming responses and markdown rendering.
