# Yash's AI Chatbot

An interactive AI chatbot built with FastAPI (backend) and React (frontend) that can engage in conversations using both text and voice input. The assistant is powered by OpenAI's GPT-4 and uses Whisper for speech recognition.

## Features

- AI-powered conversations using GPT-4
- Voice input support using Whisper
- Text-to-speech response using gTTS
- Real-time chat interface with React
- Responsive design
- Conversation history with context
- Global deployment with Localtunnel

## Prerequisites

- Python 3.8+
- Node.js and npm
- OpenAI API key

## Installation

1. Clone the repository:

```bash
git clone <your-repo-url>
cd homellc
```

2. Install localtunnel for global deployment:

```bash
./install_localtunnel.sh
```

3. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

4. Install Python dependencies:

```bash
pip install -r requirements.txt
```

5. Install frontend dependencies:

```bash
cd frontend
npm install
cd ..
```

6. Set up your environment variables:

Create a `.env` file in the root directory with your OpenAI API key:

```bash
# .env
OPENAI_API_KEY=your-api-key-here
```

⚠️ **Important**: Never commit your `.env` file to version control. It's already in `.gitignore`.

## Usage

### Local Development

Run both frontend and backend locally:

```bash
./run_local.sh
```

This will start:

- Backend server at `http://localhost:8000`
- Frontend development server at `http://localhost:3000`

### Global Deployment with Localtunnel

Deploy your app globally with public URLs:

```bash
./deploy_global.sh
```

This will create:

- Backend tunnel at `https://yash-backend.loca.lt`
- Frontend tunnel at `https://yash-frontend.loca.lt`

## Input Methods

- **Text Input**: Type your questions directly in the chat input
- **Voice Input**: Click the microphone button and speak your question

## API Endpoints

- `POST /api/chat` - Text-based chat
- `POST /api/voice` - Voice-based chat
- `GET /api/user_info` - Get user information
- `POST /api/clear` - Clear chat history
- `GET /api/test` - Test endpoint

## Deployment Options

1. **Local Development**: Use `./run_local.sh` for local testing
2. **Global with Localtunnel**: Use `./deploy_global.sh` for public access
3. **Custom Backend URL**: Set `REACT_APP_API_BASE` environment variable

## Troubleshooting

### Invalid Host Header Error

If you see "Invalid Host header" when accessing the frontend through localtunnel, the React development server has been configured to accept requests from localtunnel domains. The `frontend/start-react.sh` script sets the necessary environment variables:

- `DANGEROUSLY_DISABLE_HOST_CHECK=true` - Allows requests from any host
- `HOST=0.0.0.0` - Binds to all network interfaces

## License

MIT License

## Author

Yashaswa Varshney

- Email: yswa.var@icloud.com
- LinkedIn: [linkedin.com/in/yashaswa-varshney](https://linkedin.com/in/yashaswa-varshney)
- GitHub: [github.com/yswa-var](https://github.com/yswa-var)

```

```
