@echo off
cls

echo 🏦 Bank Chatbot Installation Script
echo ==================================
echo.

REM Check Python installation
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python is not installed. Please install Python 3.8+ first.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Check Node.js installation
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js is not installed. Please install Node.js 18+ first.
    echo Download from: https://nodejs.org/
    pause
    exit /b 1
)

echo ✅ Python found
python --version
echo ✅ Node.js found
node --version
echo.

REM Install Python dependencies
echo 📦 Installing Python dependencies...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo ❌ Failed to install Python dependencies
    pause
    exit /b 1
)

echo ✅ Python dependencies installed successfully
echo.

REM Install Node.js dependencies
echo 📦 Installing Node.js dependencies...
cd frontend
npm install

if %errorlevel% neq 0 (
    echo ❌ Failed to install Node.js dependencies
    pause
    exit /b 1
)

echo ✅ Node.js dependencies installed successfully
cd ..

echo.
echo 🎉 Installation completed!
echo.
echo 🚀 To start the application:
echo 1. Open terminal 1 and run: python bank_chatbot_api.py
echo 2. Open terminal 2 and run: cd frontend ^&^& npm run dev
echo 3. Open your browser and go to: http://localhost:3000
echo.
echo 📚 For more information, see README.md
echo.
pause