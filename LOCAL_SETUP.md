# Local Setup & Sharing Guide

This guide will help you run Yash's AI Chatbot locally and share it with others.

## 🚀 Quick Start (Recommended)

1. **Make the script executable and run it:**

   ```bash
   chmod +x run_local.sh
   ./run_local.sh
   ```

2. **Create a `.env` file** (if you don't have one):

   ```bash
   echo "OPENAI_API_KEY=your-openai-api-key-here" > .env
   ```

3. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000

## 📋 Manual Setup

### Prerequisites

- Python 3.8+
- Node.js 16+
- OpenAI API key

### Backend Setup

```bash
# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create .env file with your OpenAI API key
echo "OPENAI_API_KEY=your-api-key-here" > .env

# Start the backend server
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start the development server
npm start
```

## 🌐 Sharing with Others

### Option 1: Local Network Access (Same WiFi)

1. **Find your local IP address:**

   ```bash
   # On macOS/Linux
   ifconfig | grep "inet " | grep -v 127.0.0.1

   # On Windows
   ipconfig | findstr "IPv4"
   ```

2. **Update the API_BASE in frontend/src/App.js:**

   ```javascript
   const API_BASE = "http://YOUR_LOCAL_IP:8000";
   ```

3. **Start the servers with network access:**

   ```bash
   # Backend (allow external connections)
   uvicorn main:app --reload --host 0.0.0.0 --port 8000

   # Frontend (allow external connections)
   cd frontend
   REACT_APP_API_URL=http://YOUR_LOCAL_IP:8000 npm start
   ```

4. **Share the frontend URL:**
   - Others on the same network can access: `http://YOUR_LOCAL_IP:3000`

### Option 2: Internet Access (ngrok)

1. **Install ngrok:**

   ```bash
   # On macOS with Homebrew
   brew install ngrok

   # Or download from https://ngrok.com/
   ```

2. **Start your local servers** (as in Option 1)

3. **Create ngrok tunnels:**

   ```bash
   # For backend API
   ngrok http 8000

   # For frontend (in another terminal)
   ngrok http 3000
   ```

4. **Update the API_BASE in frontend/src/App.js:**

   ```javascript
   const API_BASE = "https://YOUR_NGROK_BACKEND_URL";
   ```

5. **Share the ngrok frontend URL** with anyone on the internet

### Option 3: Cloud Deployment (Recommended for Production)

#### Backend Deployment (Render/Railway/Heroku)

1. **Deploy to Render:**

   - Go to [render.com](https://render.com)
   - Create new Web Service
   - Connect your GitHub repository
   - Set build command: `pip install -r requirements.txt`
   - Set start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Add environment variable: `OPENAI_API_KEY`

2. **Deploy to Railway:**
   - Go to [railway.app](https://railway.app)
   - Create new project from GitHub
   - Add environment variable: `OPENAI_API_KEY`

#### Frontend Deployment (Netlify/Vercel)

1. **Deploy to Netlify:**

   - Go to [netlify.com](https://netlify.com)
   - Connect your GitHub repository
   - Set build settings:
     - Base directory: `frontend`
     - Build command: `npm run build`
     - Publish directory: `build`

2. **Update API URL for production:**
   - In `frontend/src/App.js`, update `API_BASE` to your deployed backend URL

## 🔧 Troubleshooting

### Common Issues

1. **Port already in use:**

   ```bash
   # Find and kill process using port 8000
   lsof -ti:8000 | xargs kill -9

   # Or use different ports
   uvicorn main:app --reload --host 0.0.0.0 --port 8001
   ```

2. **CORS errors:**

   - The backend already has CORS configured for all origins
   - If issues persist, check that the API_BASE URL is correct

3. **OpenAI API errors:**

   - Verify your API key is correct
   - Check your OpenAI account has sufficient credits

4. **Audio recording issues:**
   - Ensure microphone permissions are granted
   - Try using HTTPS (required for microphone access in some browsers)

### Environment Variables

Create a `.env` file in the root directory:

```env
OPENAI_API_KEY=your-openai-api-key-here
```

## 📱 Mobile Access

- The frontend is responsive and works on mobile devices
- For voice features, use HTTPS (ngrok provides this)
- Test on different devices to ensure compatibility

## 🔒 Security Notes

- Never commit your `.env` file to version control
- The `.gitignore` file already excludes sensitive files
- For production, use proper environment variable management
- Consider rate limiting for public deployments

## 🎯 Next Steps

1. **Customize the chatbot personality** by editing the `SYSTEM_PROMPT` in `main.py`
2. **Add more features** like file upload, image generation, etc.
3. **Improve the UI** by modifying the CSS in `frontend/src/App.css`
4. **Add authentication** for private deployments
5. **Monitor usage** and costs with OpenAI API

## 📞 Support

If you encounter issues:

1. Check the console for error messages
2. Verify all dependencies are installed
3. Ensure your OpenAI API key is valid
4. Check network connectivity and firewall settings
