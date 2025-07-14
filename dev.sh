#!/bin/bash

# Development script for Homelx Chat App
# This script starts both the frontend and backend servers

echo "🚀 Starting Homelx Chat App Development Environment..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "⚠️  Warning: .env file not found!"
    echo "Please create a .env file with your OPENAI_API_KEY"
    echo "Example: echo 'OPENAI_API_KEY=your_key_here' > .env"
fi

# Install dependencies if needed
echo "📦 Installing dependencies..."

# Install Node.js dependencies for backend
if [ ! -d "backend/node_modules" ]; then
    echo "Installing backend Node.js dependencies..."
    cd backend && npm install && cd ..
fi

# Install Node.js dependencies for frontend
if [ ! -d "frontend/node_modules" ]; then
    echo "Installing frontend Node.js dependencies..."
    cd frontend && npm install && cd ..
fi

# Start backend server in background
echo "🔧 Starting backend server on http://localhost:8000..."
cd backend
npm run dev &
BACKEND_PID=$!
cd ..

# Wait a moment for backend to start
sleep 3

# Start frontend server
echo "🎨 Starting frontend server on http://localhost:5173..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo "✅ Both servers are running!"
echo "📱 Frontend: http://localhost:5173"
echo "🔧 Backend: http://localhost:8000"
echo ""
echo "Press Ctrl+C to stop both servers"

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    echo "✅ Servers stopped"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Wait for user to stop
wait 