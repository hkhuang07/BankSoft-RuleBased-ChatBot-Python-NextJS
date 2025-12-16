#!/bin/bash

echo "🚀 Khởi động Bank-SoftAI Enhanced..."

# Find backend file - check both locations
BACKEND_FILE=""
if [ -f "bank_chatbot_api.py" ]; then
    BACKEND_FILE="bank_chatbot_api.py"
elif [ -f "backend/bank_chatbot_api.py" ]; then
    BACKEND_FILE="backend/bank_chatbot_api.py"
else
    echo "❌ Không tìm thấy bank_chatbot_api.py"
    echo "Vui lòng đảm bảo file backend có mặt ở:">
    echo "  - ./bank_chatbot_api.py hoặc"
    echo "  - ./backend/bank_chatbot_api.py"
    exit 1
fi

echo "✅ Tìm thấy backend file: $BACKEND_FILE"

# Check if backend is running
if lsof -Pi :5000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "✅ Backend đã chạy trên port 5000"
else
    echo "🔄 Đang khởi động backend..."
    python $BACKEND_FILE &
    BACKEND_PID=$!
    sleep 3
    echo "✅ Backend đã khởi động (PID: $BACKEND_PID)"
fi

# Wait a moment for backend to start
sleep 2

# Check if we're in frontend directory
if [ ! -d "frontend" ]; then
    echo "❌ Không tìm thấy folder frontend"
    echo "Vui lòng chạy script từ thư mục gốc của dự án"
    exit 1
fi

# Navigate to frontend and start
cd frontend
echo "🔄 Đang khời động frontend..."
npm run dev &

cd ..

echo ""
echo "🎉 Ứng dụng đã khởi động!"
echo ""
echo "📍 URLs:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:5000"
echo ""
echo "🔧 Tính năng mới:"
echo "   🌙 Dark/Light mode toggle"
echo "   🌍 Multi-language (Việt/Anh)"
echo "   📝 Chat history với localStorage"
echo "   💡 Smart suggestions cho mọi menu level"
echo "   🎨 Enhanced UI/UX"
echo "   📱 Responsive design"
echo "   🛡️  Hydration error fix"
echo ""
echo "⚠️  Nếu gặp lỗi, xem: KHAC_PHUC_LOI_ENHANCED.md"
echo ""
echo "⏹️  Để dừng: Ctrl+C"
echo ""

# Keep script running
wait