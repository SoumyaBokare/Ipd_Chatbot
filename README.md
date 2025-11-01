🤖 Ultra-Advanced Kiosk Chatbot System
======================================

A comprehensive AI-powered chatbot system with multi-model support, web interface, voice capabilities, and enterprise features.

---

## 📦 QUICK SETUP FOR NEW USERS (FOR YOUR FRIEND!)

### 🎯 **Easy Setup - Ollama Local Models** (100% Free, No API Keys!)

**What you need:**
- Windows PC with Python 3.8+ installed
- Internet connection (only for initial setup)
- ~4-8 GB free disk space for models
- **NO API KEYS NEEDED!** Everything runs locally

**Steps:**

1. **Download/Clone this project**
   ```powershell
   git clone <repository-url>
   cd chatbot
   ```

2. **Install Ollama** (AI model runner)
   - Download from: https://ollama.com/download
   - Run the installer
   - Ollama will run in the background automatically

3. **Download AI models** (one-time setup)
   ```powershell
   # Download the main model (takes 5-10 minutes, ~4.7GB)
   ollama pull llama3.1:8b
   
   # Optional: Download lightweight fallback models
   ollama pull gemma:2b
   ollama pull phi3:mini
   ```

4. **Install Python dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

5. **Run the chatbot!**
   
   **Option A: Web Interface (Recommended)**
   ```powershell
   python web_app.py
   ```
   Then open http://127.0.0.1:5000 in your browser

   **Option B: Terminal Chat**
   ```powershell
   python main.py
   ```

**That's it! 🎉** The chatbot runs 100% locally on your machine!

**💡 Advantages of Ollama:**
- ✅ Completely FREE forever
- ✅ No API keys or accounts needed
- ✅ Works offline (after initial model download)
- ✅ Privacy - your data never leaves your computer
- ✅ No usage limits or costs

---

### 🔧 **Full Setup - All Models** (For advanced users)

If you want access to all 9 AI providers (Ollama, Claude, local models, etc.):

1. **Clone the repository**
   ```powershell
   git clone <repository-url>
   cd chatbot
   ```

2. **Run the interactive setup**
   ```powershell
   python setup_models.py
   ```
   This will guide you through:
   - Installing dependencies
   - Choosing which AI providers to use
   - Setting up API keys
   - Testing your configuration

3. **Start the chatbot**
   ```powershell
   # For web interface:
   python web_app.py
   
   # For terminal interface:
   python main.py
   ```

---

### 🆘 **Troubleshooting Common Issues**

**Problem: "Python not found"**
- Install Python from https://www.python.org/downloads/
- Make sure to check "Add Python to PATH" during installation

**Problem: "pip: command not found"**
- Reinstall Python with "Add to PATH" option
- Or use: `python -m pip install -r requirements.txt`

**Problem: "ollama: command not found"**
- Make sure Ollama is installed from https://ollama.com/download
- Restart your terminal/PowerShell after installation
- Check if Ollama is running: open Task Manager and look for "ollama"

**Problem: "Connection refused" or "Ollama not responding"**
- Start Ollama service: Just run `ollama serve` in a terminal
- Or restart your computer (Ollama should auto-start)
- Check if Ollama is running on http://localhost:11434

**Problem: "Model not found"**
- Pull the model first: `ollama pull llama3.1:8b`
- Check available models: `ollama list`
- Make sure model name matches exactly (case-sensitive)

**Problem: "Module not found" errors**
- Run: `pip install -r requirements.txt`
- If still errors, try: `pip install --upgrade -r requirements.txt`

**Problem: Web page won't load**
- Make sure the server started successfully (check console for errors)
- Try a different browser
- Check if another program is using port 5000
- Try: `python web_app.py` and look for error messages

**Problem: Chatbot responses are slow**
- First response is slower (model loading into memory)
- Try a smaller/faster model: `llama3.2:1b` or `gemma:2b`
- Close other heavy applications to free up RAM
- Recommended: 8GB+ RAM for best performance

**Problem: Out of memory errors**
- Use a smaller model: `ollama pull gemma:2b` (only 1.5GB)
- Close other applications
- Restart your computer

---

### 📋 **Files Needed to Share**

If sending this to a friend, they need these files:

**Core Files (Required):**
- `main.py` (chatbot core logic)
- `web_app.py` (web interface)
- `requirements.txt` (Python dependencies)
- `templates/` folder (HTML templates)
- `static/` folder (CSS, JS files)
- `README.md` (this file)

**Optional Files:**
- `model_config_examples.py` (configuration examples)
- `setup_models.py` (interactive setup script)
- `test_models.py` (model testing)
- `.env` (environment variables - **NOT NEEDED for Ollama!**)

**What to tell your friend:**
1. Install Ollama from https://ollama.com/download
2. Run: `ollama pull llama3.1:8b`
3. Run: `pip install -r requirements.txt`
4. Run: `python web_app.py`
5. Open http://127.0.0.1:5000

**⚠️ NO API KEYS NEEDED!** Since you're using Ollama (local models), your friend doesn't need any API keys or accounts. Everything runs locally!

---

### 🚀 **Available Models** (Your friend can choose)

**Recommended models:**
- `llama3.1:8b` - Main model, balanced (4.7GB)
- `gemma:2b` - Fast and lightweight (1.5GB)
- `phi3:mini` - Good for coding tasks (2.2GB)
- `llama3.2:1b` - Ultra-fast for quick responses (1.3GB)
- `neural-chat` - Conversational model (4.1GB)

To switch models in the web interface:
- Use the model dropdown menu
- Or edit `web_app.py` line 30 to change the default

---

## 🚀 Features

- **🧠 Multi-Model AI Support**: 9 different AI providers with automatic failover
- **🌐 Web Interface**: Modern Flask-based web UI with real-time chat
- **🌍 Multi-Language**: 50+ languages supported with translation
- **♿ Accessibility**: Full WCAG compliance and voice support
- **📊 Analytics**: Advanced usage tracking and insights
- **🔒 Security**: Enterprise-grade security features
- **⚡ Performance**: Smart caching and optimization

## 🤖 Supported AI Models

### 1. **OLLAMA** (Local Models) ⭐ Recommended for beginners
- **Models**: `llama3.2:latest`, `neural-chat`, `codellama`, `mistral:latest`
- **Setup**: Install Ollama and pull models
- **Cost**: Free
- **Internet**: Not required after setup

### 2. **OpenAI** (GPT Models) ⭐ Most reliable
- **Models**: `gpt-4o`, `gpt-4`, `gpt-3.5-turbo`
- **Setup**: Requires `OPENAI_API_KEY`
- **Cost**: Pay per token
- **Internet**: Required

### 3. **Anthropic** (Claude Models) ⭐ Most capable
- **Models**: `claude-3-5-sonnet-20241022`, `claude-3-opus-20240229`, `claude-3-haiku-20240307`
- **Setup**: Requires `ANTHROPIC_API_KEY`
- **Cost**: Pay per token
- **Internet**: Required

### 4. **LOCAL** (Transformers) ⭐ Completely offline
- **Models**: `microsoft/DialoGPT-medium`, `gpt2`, `distilgpt2`
- **Setup**: Automatic download via Hugging Face
- **Cost**: Free
- **Internet**: Only for initial model download

### 5. **Hugging Face Hub**
- **Models**: `microsoft/DialoGPT-large`, `facebook/blenderbot-1B-distill`
- **Setup**: Requires `HUGGINGFACE_API_TOKEN`
- **Cost**: Free tier available
- **Internet**: Required

### 6. **Cohere**
- **Models**: `command`, `command-light`, `command-nightly`
- **Setup**: Requires `COHERE_API_KEY`
- **Cost**: Free tier available
- **Internet**: Required

### 7. **Google (PaLM/Gemini)**
- **Models**: `gemini-1.5-pro`, `gemini-1.5-flash`, `gemini-pro`
- **Setup**: Requires `GOOGLE_API_KEY`
- **Cost**: Free tier available
- **Internet**: Required

### 8. **Mistral AI**
- **Models**: `mistral-large-latest`, `mistral-medium-latest`, `mistral-small-latest`
- **Setup**: Requires `MISTRAL_API_KEY`
- **Cost**: Pay per token
- **Internet**: Required

### 9. **Replicate**
- **Models**: `meta/llama-2-70b-chat`, `meta/llama-2-13b-chat`
- **Setup**: Requires `REPLICATE_API_TOKEN`
- **Cost**: Pay per second
- **Internet**: Required

## 🛠️ Quick Start

### Option 1: Easy Setup Script (Recommended)
```powershell
# Run the interactive setup
python setup_models.py
```

### Option 2: Manual Setup

```powershell
# 1. Activate virtual environment (if using one)
.\ipd_chatbot\Scripts\activate

# 2. Install core dependencies
pip install -r requirements.txt

# 3. Choose your AI provider and install specific dependencies:

# For Ollama (Local, Free)
ollama serve
ollama pull neural-chat

# For OpenAI
pip install langchain-openai
# Set OPENAI_API_KEY in environment

# For local transformers models
pip install transformers torch

# 4. Run the application
python main.py              # Terminal interface
# OR
python web_app.py           # Web interface (http://127.0.0.1:5000)
```

## 🔑 Environment Variables

Create a `.env` file or set these in your system environment:

```bash
# OpenAI (GPT models)
OPENAI_API_KEY=your_openai_api_key_here

# Anthropic (Claude models)  
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Hugging Face Hub
HUGGINGFACE_API_TOKEN=your_huggingface_token_here

# Cohere
COHERE_API_KEY=your_cohere_api_key_here

# Google (PaLM/Gemini)
GOOGLE_API_KEY=your_google_api_key_here

# Mistral AI
MISTRAL_API_KEY=your_mistral_api_key_here

# Replicate
REPLICATE_API_TOKEN=your_replicate_token_here
```

## 📁 Project Structure

```
chatbot/
├── main.py                    # Main terminal chatbot
├── web_app.py                # Flask web application  
├── model_config_examples.py   # Configuration examples
├── setup_models.py           # Interactive setup script
├── test_models.py            # Model testing script
├── requirements.txt          # Python dependencies
├── templates/                # Web UI templates
├── static/                   # CSS, JS, assets
└── logs/                     # Application logs
```

## 🧪 Testing Models

Test your model setup:

```powershell
python test_models.py
```

## 📖 Configuration Examples

See `model_config_examples.py` for detailed configuration examples for each provider.

## 🎯 Recommended Setups

### 🏠 **Home/Personal Use**
```python
# Ollama + Local models (Free, Privacy-focused)
config = KioskConfig(
    primary_model_provider=ModelProvider.OLLAMA,
    primary_model_name="llama3.2:latest",
    fallback_models=[
        (ModelProvider.LOCAL, "microsoft/DialoGPT-medium")
    ]
)
```

### 💼 **Business/Production**
```python
# OpenAI + Anthropic with local fallback
config = KioskConfig(
    primary_model_provider=ModelProvider.OPENAI,
    primary_model_name="gpt-4",
    fallback_models=[
        (ModelProvider.ANTHROPIC, "claude-3-haiku-20240307"),
        (ModelProvider.LOCAL, "microsoft/DialoGPT-medium")
    ]
)
```

### 💰 **Budget-Friendly**
```python
# Local + Free tier models only
config = KioskConfig(
    primary_model_provider=ModelProvider.LOCAL,
    primary_model_name="microsoft/DialoGPT-medium",
    fallback_models=[
        (ModelProvider.HUGGINGFACE, "microsoft/DialoGPT-large")
    ]
)
```

## 🌐 Web Interface

Access the modern web interface at `http://127.0.0.1:5000` after running:

```powershell
python web_app.py
```

## 📊 Features

- **Real-time chat interface**
- **Model selection dropdown**  
- **Language translation**
- **Voice input/output**
- **Usage analytics**
- **Accessibility features**

## 🆘 Troubleshooting

### Common Issues:

1. **"Module not found" errors**: Run `python setup_models.py` to install dependencies
2. **API key errors**: Set environment variables in `.env` file
3. **Ollama connection failed**: Start Ollama service: `ollama serve`
4. **Model download slow**: Local models download on first use

### Getting Help:

1. Check `logs/` directory for detailed error logs
2. Run `python test_models.py` to diagnose model issues
3. See `model_config_examples.py` for working configurations

## 🚀 Advanced Features

- **Multi-language support** (50+ languages)
- **Voice input/output**
- **Analytics dashboard**
- **Custom model integration**
- **Enterprise security**
- **Accessibility compliance**

## 📄 License

This project is open source. See configuration examples and documentation for implementation details.
- If `main.py` can't initialize models because optional packages or APIs are missing, the web UI will still load but `/api/chat` will return an error explaining the chatbot isn't initialized. Check server logs to diagnose.
- For production, consider adding process supervision and HTTPS.
