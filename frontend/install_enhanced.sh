#!/bin/bash

echo "🚀 Cài đặt dependencies cho frontend Bank-SoftAI Enhanced..."

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js chưa được cài đặt. Vui lòng cài đặt Node.js trước."
    exit 1
fi

# Check if npm is installed
if ! command -v npm &> /dev/null; then
    echo "❌ npm chưa được cài đặt. Vui lòng cài đặt npm trước."
    exit 1
fi

echo "✅ Node.js và npm đã sẵn sàng"

# Install dependencies
echo "📦 Đang cài đặt dependencies..."
npm install

if [ $? -eq 0 ]; then
    echo "✅ Dependencies đã được cài đặt thành công!"
    
    echo ""
    echo "🎉 Hoàn thành! Để chạy ứng dụng:"
    echo "   1. Chạy backend trước: python bank_chatbot_api.py"
    echo "   2. Chạy frontend: npm run dev"
    echo "   3. Mở trình duyệt: http://localhost:3000"
    echo ""
    echo "✨ Tính năng mới:"
    echo "   🌙 Dark/Light mode"
    echo "   🌍 Multi-language (Việt/Anh)"
    echo "   📝 Chat history với localStorage"
    echo "   💡 Gợi ý trả lời cho mọi menu level"
    echo "   🎨 UI/UX cải tiến"
else
    echo "❌ Có lỗi khi cài đặt dependencies"
    exit 1
fi