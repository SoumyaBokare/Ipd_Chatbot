@echo off
echo ======================================================================
echo                🚀 ULTRA-ADVANCED KIOSK CHATBOT WEB LAUNCHER
echo ======================================================================
echo.

echo 🔍 Checking Python environment...
python --version
if errorlevel 1 (
    echo ❌ Python not found! Please install Python 3.8+ and try again.
    pause
    exit /b 1
)

echo.
echo 🔍 Checking if virtual environment exists...
if exist "ipd_chatbot\Scripts\activate.bat" (
    echo ✅ Virtual environment found, activating...
    call ipd_chatbot\Scripts\activate.bat
) else (
    echo ⚠️  No virtual environment found. Creating one...
    python -m venv ipd_chatbot
    call ipd_chatbot\Scripts\activate.bat
    echo ✅ Virtual environment created and activated.
)

echo.
echo 📦 Installing/updating dependencies...
pip install --upgrade pip
pip install -r requirements.txt

echo.
echo 🔧 Checking if Ollama is running...
curl -s http://localhost:11434/api/tags >nul 2>&1
if errorlevel 1 (
    echo ⚠️  Ollama not detected. Please ensure:
    echo    1. Ollama is installed ^(download from https://ollama.com^)
    echo    2. Ollama service is running: 'ollama serve'
    echo    3. Neural-chat model is pulled: 'ollama pull neural-chat'
    echo.
    echo 💡 You can continue anyway, but AI features may not work.
    set /p choice="Continue? (y/n): "
    if /i not "%choice%"=="y" (
        echo Exiting...
        pause
        exit /b 1
    )
) else (
    echo ✅ Ollama is running!
)

echo.
echo 🌐 Starting Ultra-Advanced Kiosk Web Server...
echo ✨ Once started, access the chatbot at: http://localhost:5000
echo 🔧 Press Ctrl+C to stop the server
echo.

python web_app.py

echo.
echo 👋 Thank you for using Ultra-Advanced Kiosk Chatbot!
pause