# 🤖 Simple OpenAI Chatbot

A simplified version of the chatbot that uses **only OpenAI GPT models**. No complex setup, just OpenAI.

## 🚀 Quick Start (Windows)

### Option 1: One-Click Start
1. **Double-click `start_simple.bat`** - that's it! 
2. Opens automatically at `http://127.0.0.1:5000`

### Option 2: Manual Setup
```powershell
# 1. Install dependencies
pip install -r simple_requirements.txt

# 2. Your API key is already set in .env file:
# OPENAI_API_KEY=sk-1234567890abcdef1234567890abcdef12345678

# 3. Start web interface
python simple_web_chat.py

# 4. Open http://127.0.0.1:5000 in your browser
```

### Option 3: Terminal Chat
```powershell
# Chat directly in terminal
python simple_openai_chat.py
```

## 🎯 What's Included

- **✅ OpenAI GPT-3.5-turbo** (primary model)
- **✅ OpenAI GPT-4o-mini** (fallback) 
- **✅ OpenAI GPT-4** (fallback)
- **✅ Web interface** (modern chat UI)
- **✅ Terminal interface** (simple text chat)
- **✅ Your API key** (already configured)

## 🚫 What's Removed

- ❌ Multiple model providers (Ollama, Anthropic, etc.)
- ❌ Complex configuration options
- ❌ Voice features
- ❌ Advanced analytics
- ❌ Model selection buttons

## 📁 Files for Simple Setup

- `simple_web_chat.py` - Web interface server
- `simple_openai_chat.py` - Terminal chat
- `templates/simple_chat.html` - Web UI
- `simple_requirements.txt` - Dependencies
- `start_simple.bat` - One-click startup
- `.env` - Your API key (already set)

## 💰 Cost Information

**OpenAI GPT-3.5-turbo** (default):
- ~$0.002 per 1,000 tokens
- Very affordable for normal chat usage

**OpenAI GPT-4** (fallback):
- ~$0.06 per 1,000 tokens  
- Only used if GPT-3.5 fails

## 🛠️ Troubleshooting

### "API key not found" error:
- Check that `.env` file exists with your key
- Restart the application

### "Invalid API key" error:
- Verify your OpenAI API key is correct
- Check you have credits on your OpenAI account

### Connection issues:
- Check your internet connection
- Verify OpenAI service status

### Dependencies error:
```powershell
pip install --upgrade pip
pip install -r simple_requirements.txt
```

## 🔑 API Key Management

Your API key is stored in `.env`:
```
OPENAI_API_KEY=sk-1234567890abcdef1234567890abcdef12345678
```

To change it, edit the `.env` file or create a new one.

## 🎉 That's It!

This simplified version removes all the complexity and gives you a clean, working OpenAI chatbot with both web and terminal interfaces.

**Just run `start_simple.bat` and start chatting!** 🚀