@echo off
echo 🚀 Khởi động Bank-SoftAI Enhanced...

REM Check if backend file exists in both locations
set BACKEND_FILE=
if exist "bank_chatbot_api.py" (
    set BACKEND_FILE=bank_chatbot_api.py
    echo ✅ Tìm thấy backend file: %BACKEND_FILE%
) else if exist "backend\bank_chatbot_api.py" (
    set BACKEND_FILE=backend\bank_chatbot_api.py
    echo ✅ Tìm thấy backend file: %BACKEND_FILE%
) else (
    echo ❌ Không tìm thấy bank_chatbot_api.py
    echo Vui lòng đảm bảo file backend có mặt ở:
    echo   - .\bank_chatbot_api.py hoặc
    echo   - .\backend\bank_chatbot_api.py
    pause
    exit /b 1
)

REM Check if backend is already running
netstat -an | findstr ":5000" >nul
if %errorlevel% equ 0 (
    echo ✅ Backend đã chạy trên port 5000
) else (
    echo 🔄 Đang khởi động backend...
    start "Backend API" cmd /k "python %BACKEND_FILE%"
    timeout /t 3 >nul
    echo ✅ Backend đã khởi động
)

REM Wait a moment for backend to start
timeout /t 2 >nul

REM Check if frontend directory exists
if not exist "frontend" (
    echo ❌ Không tìm thấy folder frontend
    echo Vui lòng chạy script từ thư mục gốc của dự án
    pause
    exit /b 1
)

REM Start frontend
cd frontend
echo 🔄 Đang khời động frontend...
start "Frontend NextJS" cmd /k "npm run dev"
cd ..

echo.
echo 🎉 Ứng dụng đã khởi động!
echo.
echo 📍 URLs:
echo    Frontend: http://localhost:3000
echo    Backend API: http://localhost:5000
echo.
echo 🔧 Tính năng mới:
echo    🌙 Dark/Light mode toggle
echo    🌍 Multi-language (Việt/Anh)
echo    📝 Chat history với localStorage
echo    💡 Smart suggestions cho mọi menu level
echo    🎨 Enhanced UI/UX
echo    📱 Responsive design
echo    🛡️  Hydration error fix
echo.
echo ⚠️  Nếu gặp lỗi, xem: KHAC_PHUC_LOI_ENHANCED.md
echo.
echo ⏹️  Để dừng: Đóng các cửa sổ cmd
echo.

pause