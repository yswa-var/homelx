#!/bin/bash

echo "🌐 Finding your local IP address for network sharing..."

# Get local IP address
LOCAL_IP=$(ifconfig | grep "inet " | grep -v 127.0.0.1 | awk '{print $2}' | head -1)

if [ -z "$LOCAL_IP" ]; then
    echo "❌ Could not find local IP address"
    echo "Try running: ifconfig | grep 'inet '"
    exit 1
fi

echo "✅ Your local IP address is: $LOCAL_IP"
echo ""
echo "📱 To share with others on the same network:"
echo "1. Update frontend/src/App.js:"
echo "   const API_BASE = \"http://$LOCAL_IP:8000\";"
echo ""
echo "2. Start your servers:"
echo "   ./run_local.sh"
echo ""
echo "3. Share this URL with others:"
echo "   http://$LOCAL_IP:3000"
echo ""
echo "🔒 Note: This only works for devices on the same WiFi network" 