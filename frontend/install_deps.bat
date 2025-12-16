@echo off
cls

echo 📦 Cài đặt dependencies cho Bank Chatbot Frontend
echo ================================================

REM Check Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js không được cài đặt. Vui lòng cài đặt Node.js 18+ trước.
    echo    Tải từ: https://nodejs.org/
    pause
    exit /b 1
)

echo ✅ Node.js found
node --version
echo ✅ npm found
npm --version
echo.

REM Cài đặt dependencies
echo 📦 Cài đặt dependencies...
npm install

if %errorlevel% neq 0 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo ✅ Dependencies installed successfully!
echo.
echo 🚀 Để chạy development server:
echo    cd frontend
echo    npm run dev
echo.
echo 🌐 Frontend sẽ chạy tại: http://localhost:3000
echo.
pause