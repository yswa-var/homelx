#!/bin/bash

echo "🌍 Deploying Yash's AI Chatbot globally with Localtunnel..."

# Check if localtunnel is installed
if ! command -v lt &> /dev/null; then
    echo "❌ localtunnel is not installed. Please install it first:"
    echo "   npm install -g localtunnel"
    echo "   or visit https://theboroer.github.io/localtunnel-www/"
    exit 1
fi

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "Please create a .env file with your OPENAI_API_KEY:"
    echo "OPENAI_API_KEY=your-api-key-here"
    exit 1
fi

echo "🚀 Starting local servers..."
./run_local.sh &
LOCAL_PID=$!

# Wait for servers to start
echo "⏳ Waiting for servers to start..."
sleep 15

echo "🌐 Creating public tunnels with Localtunnel..."
echo "📱 This will give you public URLs that work globally!"
echo ""

# Start localtunnel for backend (port 8000)
echo "🔧 Creating tunnel for backend (port 8000)..."
lt --port 8000 --subdomain yash-backend &
BACKEND_TUNNEL_PID=$!

# Wait a moment for backend tunnel to establish
sleep 5

# Start localtunnel for frontend (port 3000)
echo "🎨 Creating tunnel for frontend (port 3000)..."
lt --port 3000 --subdomain yash-frontend &
FRONTEND_TUNNEL_PID=$!

echo ""
echo "✅ Tunnels are being created..."
echo "🔧 Backend tunnel: https://yash-backend.loca.lt"
echo "🎨 Frontend tunnel: https://yash-frontend.loca.lt"
echo ""
echo "⚠️  Note: You'll need to update the API_BASE in frontend/src/App.js"
echo "   to point to your backend tunnel URL"
echo ""
echo "Press Ctrl+C to stop all servers and tunnels"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping all servers and tunnels..."
    kill $LOCAL_PID 2>/dev/null
    kill $BACKEND_TUNNEL_PID 2>/dev/null
    kill $FRONTEND_TUNNEL_PID 2>/dev/null
    pkill -f "lt" 2>/dev/null
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Wait for background processes
wait 