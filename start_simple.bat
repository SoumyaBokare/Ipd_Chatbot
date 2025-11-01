@echo off
echo 🤖 Simple OpenAI Chatbot Startup
echo ================================

echo.
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python first.
    pause
    exit /b 1
)

echo ✅ Python found

echo.
echo Installing dependencies...
pip install -r simple_requirements.txt

if errorlevel 1 (
    echo ❌ Failed to install dependencies
    pause
    exit /b 1
)

echo ✅ Dependencies installed

echo.
echo Checking API key...
if not exist .env (
    echo ❌ .env file not found!
    echo Creating .env file with your API key...
    echo OPENAI_API_KEY=sk-1234567890abcdef1234567890abcdef12345678 > .env
    echo ✅ .env file created
) else (
    echo ✅ .env file exists
)

echo.
echo 🚀 Starting OpenAI Chatbot Web Server...
echo 🌐 Open http://127.0.0.1:5000 in your browser
echo 🛑 Press Ctrl+C to stop
echo.

python simple_web_chat.py

echo.
echo 👋 Chatbot stopped
pause