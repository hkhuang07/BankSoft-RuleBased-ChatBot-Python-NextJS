#!/bin/bash

echo "📦 Cài đặt dependencies cho Bank Chatbot Frontend"
echo "================================================"

# Kiểm tra Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js không được cài đặt. Vui lòng cài đặt Node.js 18+ trước."
    echo "   Tải từ: https://nodejs.org/"
    exit 1
fi

echo "✅ Node.js found: $(node --version)"
echo "✅ npm found: $(npm --version)"
echo ""

# Cài đặt dependencies
echo "📦 Cài đặt dependencies..."
npm install

if [ $? -eq 0 ]; then
    echo "✅ Dependencies installed successfully!"
    echo ""
    echo "🚀 Để chạy development server:"
    echo "   cd frontend"
    echo "   npm run dev"
    echo ""
    echo "🌐 Frontend sẽ chạy tại: http://localhost:3000"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi