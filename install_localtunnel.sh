#!/bin/bash

echo "📦 Installing Localtunnel for global deployment..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js first:"
    echo "   Visit https://nodejs.org/ to download and install Node.js"
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm is not installed. Please install npm first."
    exit 1
fi

echo "✅ Node.js and npm are installed"

# Install localtunnel globally
echo "📥 Installing localtunnel globally..."
npm install -g localtunnel

# Verify installation
if command -v lt &> /dev/null; then
    echo "✅ Localtunnel installed successfully!"
    echo "🌐 You can now use ./deploy_global.sh to deploy your app globally"
else
    echo "❌ Failed to install localtunnel. Please try again manually:"
    echo "   npm install -g localtunnel"
    exit 1
fi 