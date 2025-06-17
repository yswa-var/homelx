# Deployment Guide

This project consists of two components:
1. **Frontend**: React application (deploy to Netlify)
2. **Backend**: FastAPI application (deploy to Render/Railway/Heroku)

## Frontend Deployment (Netlify)

The frontend is already configured for Netlify deployment with `netlify.toml`.

### Steps:
1. Push your code to GitHub
2. Connect your repository to Netlify
3. Netlify will automatically detect the configuration and build the React app
4. The build will use the `frontend` directory as the base and run `npm run build`

### Configuration:
- **Base directory**: `frontend`
- **Build command**: `npm run build`
- **Publish directory**: `build`
- **Node version**: 18

## Backend Deployment

### Option 1: Render (Recommended)

1. Go to [render.com](https://render.com)
2. Create a new Web Service
3. Connect your GitHub repository
4. Configure:
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - **Python Version**: 3.10.12

### Option 2: Railway

1. Go to [railway.app](https://railway.app)
2. Create a new project from GitHub
3. Railway will auto-detect the Python app
4. Set environment variables as needed

### Option 3: Heroku

1. Create a `Procfile`:
   ```
   web: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

2. Deploy using Heroku CLI or GitHub integration

## Environment Variables

Set these environment variables in your backend deployment:

- `OPENAI_API_KEY`: Your OpenAI API key

## Troubleshooting

### openai-whisper Installation Issues

If you encounter issues with `openai-whisper` installation:

1. Try running the `install_dependencies.sh` script
2. Use a different version: `openai-whisper==20230918`
3. Install dependencies separately:
   ```bash
   pip install --no-deps openai-whisper==20231117
   pip install torch torchaudio
   ```

### Frontend-Backend Communication

Make sure to update the frontend API endpoint to point to your deployed backend URL.

## Local Development

1. **Backend**: 
   ```bash
   pip install -r requirements.txt
   uvicorn main:app --reload
   ```

2. **Frontend**:
   ```bash
   cd frontend
   npm install
   npm start
   ``` 