#!/bin/bash

# Bank Chatbot Installation Script
# Script cài đặt tự động cho Bank Chatbot Website

echo "🏦 Bank Chatbot Installation Script"
echo "=================================="
echo ""

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check Python installation
if command_exists python3; then
    PYTHON_CMD="python3"
elif command_exists python; then
    PYTHON_CMD="python"
else
    echo "❌ Python is not installed. Please install Python 3.8+ first."
    exit 1
fi

# Check Node.js installation
if command_exists node; then
    NODE_CMD="node"
elif command_exists nodejs; then
    NODE_CMD="nodejs"
else
    echo "❌ Node.js is not installed. Please install Node.js 18+ first."
    exit 1
fi

echo "✅ Python found: $($PYTHON_CMD --version)"
echo "✅ Node.js found: $(node --version)"
echo ""

# Install Python dependencies
echo "📦 Installing Python dependencies..."
$PYTHON_CMD -m pip install flask flask-cors

if [ $? -eq 0 ]; then
    echo "✅ Python dependencies installed successfully"
else
    echo "❌ Failed to install Python dependencies"
    exit 1
fi

echo ""

# Install Node.js dependencies
echo "📦 Installing Node.js dependencies..."
cd frontend
npm install

if [ $? -eq 0 ]; then
    echo "✅ Node.js dependencies installed successfully"
else
    echo "❌ Failed to install Node.js dependencies"
    exit 1
fi

cd ..

echo ""
echo "🎉 Installation completed!"
echo ""
echo "🚀 To start the application:"
echo "1. Open terminal 1 and run: python bank_chatbot_api.py"
echo "2. Open terminal 2 and run: cd frontend && npm run dev"
echo "3. Open your browser and go to: http://localhost:3000"
echo ""
echo "📚 For more information, see README.md"