@echo off
echo 🚀 Cài đặt dependencies cho frontend Bank-SoftAI Enhanced...

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js chưa được cài đặt. Vui lòng cài đặt Node.js trước.
    pause
    exit /b 1
)

REM Check if npm is installed
npm --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ npm chưa được cài đặt. Vui lòng cài đặt npm trước.
    pause
    exit /b 1
)

echo ✅ Node.js và npm đã sẵn sàng

REM Install dependencies
echo 📦 Đang cài đặt dependencies...
npm install

if %errorlevel% equ 0 (
    echo ✅ Dependencies đã được cài đặt thành công!
    
    echo.
    echo 🎉 Hoàn thành! Để chạy ứng dụng:
    echo    1. Chạy backend trước: python bank_chatbot_api.py
    echo    2. Chạy frontend: npm run dev
    echo    3. Mở trình duyệt: http://localhost:3000
    echo.
    echo ✨ Tính năng mới:
    echo    🌙 Dark/Light mode
    echo    🌍 Multi-language (Việt/Anh)
    echo    📝 Chat history với localStorage
    echo    💡 Gợi ý trả lời cho mọi menu level
    echo    🎨 UI/UX cải tiến
) else (
    echo ❌ Có lỗi khi cài đặt dependencies
    pause
    exit /b 1
)

pause