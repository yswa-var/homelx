# Backend API Documentation

## Setup

1. Install dependencies:

```bash
pip install -r ../requirements.txt
```

2. Create a `.env` file in the backend directory with your OpenAI API key:

```
OPENAI_API_KEY=sk-proj-1qpo...
```

3. Run the server:

```bash
uvicorn main:app --reload
```

## API Endpoints

### POST /transcribe

Transcribes audio using OpenAI Whisper.

**Request:** Audio file upload (multipart/form-data)
**Response:**

```json
{
  "text": "transcribed text"
}
```

### POST /chat

Chats with GPT-4o using conversation context.

**Request:**

```json
{
  "message": "user message",
  "conversationId": "optional-conversation-id"
}
```

**Response:**

```json
{
  "reply": "AI response",
  "conversationId": "new-conversation-id"
}
```

### POST /tts

Converts text to speech using OpenAI TTS-1.

**Request:**

```json
{
  "text": "text to convert to speech"
}
```

**Response:** Audio file (MP3 format)

## Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key (required)
