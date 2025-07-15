#!/bin/bash

# Frontend Deployment Helper Script
# This script helps prepare the frontend for Vercel deployment

echo "🚀 Preparing frontend for Vercel deployment..."

# Check if we're in the right directory
if [ ! -f "frontend/package.json" ]; then
    echo "❌ Error: Please run this script from the root directory"
    exit 1
fi

# Check if backend URL is configured
echo "📋 Checking frontend configuration..."

if grep -q "your-render-app-name.onrender.com" frontend/src/config.js; then
    echo "⚠️  Warning: Backend URL not configured!"
    echo ""
    echo "Please update frontend/src/config.js with your actual Render backend URL:"
    echo "1. Open frontend/src/config.js"
    echo "2. Replace 'https://your-render-app-name.onrender.com' with your actual URL"
    echo "3. Example: 'https://homelx-backend.onrender.com'"
    echo ""
    read -p "Press Enter after updating the config file..."
fi

# Test the build
echo "🔨 Testing frontend build..."
cd frontend
npm install
npm run build

if [ $? -eq 0 ]; then
    echo "✅ Frontend builds successfully!"
    echo "📁 Build output: frontend/dist/"
else
    echo "❌ Frontend build failed!"
    exit 1
fi

cd ..

echo ""
echo "🎉 Frontend is ready for deployment!"
echo ""
echo "📋 Next steps:"
echo "1. Push your code to Git: git add . && git commit -m 'Ready for Vercel deployment' && git push"
echo "2. Go to https://vercel.com/dashboard"
echo "3. Click 'New Project'"
echo "4. Import your repository"
echo "5. Vercel will auto-detect the configuration from vercel.json"
echo "6. Click 'Deploy'"
echo ""
echo "🔗 After deployment, your app will be available at: https://your-app.vercel.app" 