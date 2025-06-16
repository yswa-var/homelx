# AI Voice Assistant

An interactive AI voice assistant built with Streamlit that can engage in conversations using both text and voice input. The assistant is powered by OpenAI's GPT-4 and uses Whisper for speech recognition.

## Features

- AI-powered conversations using GPT-4
- Voice input support using Whisper
- Text-to-speech response using gTTS
- Real-time chat interface
- Responsive design
- Conversation history with context

## Prerequisites

- Python 3.8+
- OpenAI API key
- Streamlit account

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yswa-var/homelx.git
cd homelx
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Set up your environment variables:

Create a `.env` file in the root directory with your OpenAI API key:

```bash
# .env
OPENAI_API_KEY=your-api-key-here
```

For Streamlit deployment, create a `.streamlit/secrets.toml` file:

```toml
# .streamlit/secrets.toml
openai_api_key = "your-api-key-here"
```

⚠️ **Important**: Never commit your `.env` file or `.streamlit/secrets.toml` file to version control. They are already in `.gitignore`.

## Usage

Run the Streamlit app:

```bash
streamlit run app.py
```

The app will be available at `http://localhost:8501`

## Input Methods

- **Text Input**: Type your questions directly in the text area
- **Voice Input**: Click the record button and speak your question (6-second recording window)

## License

MIT License

## Author

Yashaswa Varshney

- Email: yswa.var@icloud.com
- LinkedIn: [linkedin.com/in/yashaswa-varshney](https://linkedin.com/in/yashaswa-varshney)
- GitHub: [github.com/yswa-var](https://github.com/yswa-var)

```

```
