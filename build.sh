#!/bin/bash

# Build script for Homelx Chat App
# This script builds the frontend for production deployment

echo "🏗️  Building Homelx Chat App for Production..."

# Check if we're in the right directory
if [ ! -f "package.json" ]; then
    echo "❌ Error: Please run this script from the root directory"
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."

# Install Node.js dependencies
if [ ! -d "frontend/node_modules" ]; then
    echo "Installing Node.js dependencies..."
    npm install
fi

# Build frontend
echo "🔨 Building frontend..."
npm run build:frontend

# Check if build was successful
if [ -d "frontend/dist" ]; then
    echo "✅ Frontend built successfully!"
    echo "📁 Build output: frontend/dist/"
    echo ""
    echo "🚀 Ready for deployment!"
    echo "The backend will serve the frontend from the dist folder"
else
    echo "❌ Frontend build failed!"
    exit 1
fi

echo ""
echo "📋 Next steps:"
echo "1. Push your code to your Git repository"
echo "2. Deploy to Render using the render.yaml configuration"
echo "3. Set the OPENAI_API_KEY environment variable in Render" 