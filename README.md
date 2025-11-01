🤖 Ultra-Advanced Kiosk Chatbot System
======================================

A comprehensive AI-powered chatbot system with multi-model support, web interface, voice capabilities, and enterprise features.

---

## 📦 QUICK SETUP FOR NEW USERS 

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

- **🧠 Ollama Local Models**: Run AI models 100% locally and free
- **🌐 Web Interface**: Modern Flask-based web UI with real-time chat
- **🌍 Multi-Language**: 50+ languages supported with translation
- **♿ Accessibility**: Full WCAG compliance and voice support
- **📊 Analytics**: Advanced usage tracking and insights
- **🔒 Security**: Enterprise-grade security features
- **⚡ Performance**: Smart caching and optimization
- **💰 No Costs**: Completely free, no API keys or subscriptions

## 🤖 Available Ollama Models

This chatbot uses **Ollama** to run AI models locally on your computer. Here are the recommended models:

### **Recommended Models:**

1. **llama3.1:8b** ⭐ (Default)
   - Size: ~4.7GB
   - Best for: General conversation, balanced performance
   - Download: `ollama pull llama3.1:8b`

2. **gemma:2b** ⚡
   - Size: ~1.5GB
   - Best for: Fast responses, lightweight
   - Download: `ollama pull gemma:2b`

3. **phi3:mini**
   - Size: ~2.2GB
   - Best for: Coding tasks and technical questions
   - Download: `ollama pull phi3:mini`

4. **llama3.2:1b** 🚀
   - Size: ~1.3GB
   - Best for: Ultra-fast responses on slower computers
   - Download: `ollama pull llama3.2:1b`

5. **neural-chat**
   - Size: ~4.1GB
   - Best for: Natural conversations
   - Download: `ollama pull neural-chat`

6. **codellama**
   - Size: ~3.8GB
   - Best for: Programming and code generation
   - Download: `ollama pull codellama`

### **How to Download Models:**
```powershell
# Download one or more models
ollama pull llama3.1:8b
ollama pull gemma:2b

# Check which models you have installed
ollama list

# Test a model
ollama run llama3.1:8b
```

## 🛠️ Quick Start

### Simple 3-Step Setup:

```powershell
# 1. Install Ollama from https://ollama.com/download

# 2. Download a model
ollama pull llama3.1:8b

# 3. Install Python dependencies and run
pip install -r requirements.txt
python web_app.py
```

Then open **http://127.0.0.1:5000** in your browser!

### Detailed Setup:

1. **Install Ollama**
   - Download from https://ollama.com/download
   - Run the installer
   - Ollama runs automatically in the background

2. **Download AI models**
   ```powershell
   # Main model (required)
   ollama pull llama3.1:8b
   
   # Fallback models (optional but recommended)
   ollama pull gemma:2b
   ollama pull phi3:mini
   ```

3. **Install Python dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Run the chatbot**
   ```powershell
   # Web interface (recommended)
   python web_app.py
   
   # OR Terminal interface
   python main.py
   ```

## 📁 Project Structure

```
chatbot/
├── main.py                    # Main terminal chatbot
├── web_app.py                 # Flask web application  
├── requirements.txt           # Python dependencies
├── templates/                 # Web UI templates
│   ├── index.html            # Main web interface
│   └── pi_index.html         # Raspberry Pi interface
├── static/                    # CSS, JS, assets
│   ├── css/style.css
│   └── js/app.js
└── logs/                      # Application logs
```

## 🎯 How to Use

### **Web Interface:**
1. Run `python web_app.py`
2. Open http://127.0.0.1:5000
3. Select your preferred Ollama model from the dropdown
4. Start chatting!

### **Terminal Interface:**
1. Run `python main.py`
2. Type your questions
3. Get AI responses in your terminal

### **Switching Models:**
- **In Web UI**: Use the model dropdown menu at the top
- **In Code**: Edit `web_app.py` line 30 to change the default model

## 🌐 Web Interface Features

- **Real-time chat interface**
- **Model selection dropdown** - Switch between Ollama models instantly
- **Language translation** - Support for 50+ languages
- **Voice input/output** (optional)
- **Usage analytics**
- **Accessibility features**
- **Clean, modern UI**

## 💻 System Requirements

**Minimum:**
- Windows 10/11, macOS, or Linux
- Python 3.8 or higher
- 4GB RAM
- 5GB free disk space

**Recommended:**
- 8GB+ RAM (for better performance)
- 10GB+ free disk space (for multiple models)
- SSD for faster model loading

## 🆘 Troubleshooting

### Common Issues:

1. **"ollama: command not found"**
   - Install Ollama from https://ollama.com/download
   - Restart your terminal after installation

2. **"Connection refused" or "Ollama not responding"**
   - Run `ollama serve` in a terminal
   - Or restart your computer (Ollama auto-starts)
   - Check http://localhost:11434 in browser

3. **"Model not found"**
   - Download the model: `ollama pull llama3.1:8b`
   - Check installed models: `ollama list`

4. **"Module not found" errors**
   - Install dependencies: `pip install -r requirements.txt`

5. **Slow responses**
   - First response is slower (model loads into memory)
   - Use a smaller model: `gemma:2b` or `llama3.2:1b`
   - Close other applications to free RAM

6. **Out of memory errors**
   - Use a smaller model (gemma:2b uses only 1.5GB)
   - Close other applications
   - Consider upgrading RAM

### Getting Help:

- Check `logs/` directory for error logs
- Verify Ollama is running: `ollama list`
- Test a model directly: `ollama run llama3.1:8b`

## 🚀 Advanced Features

- **Multi-language support** (50+ languages via translation)
- **Voice input/output** (optional feature)
- **Usage analytics dashboard**
- **Multiple Ollama model support**
- **Automatic model failover**
- **Smart caching for faster responses**
- **Accessibility compliance**
- **100% Private** - all data stays on your computer

## ❓ FAQ

**Q: Do I need an internet connection?**
A: Only for the initial Ollama and model downloads. After that, it works completely offline!

**Q: Is this really free?**
A: Yes! 100% free forever. No hidden costs, subscriptions, or API fees.

**Q: How much does it cost to run?**
A: $0. It uses your computer's resources (CPU/RAM) which you already have.

**Q: Can I use this commercially?**
A: Yes, Ollama models are open-source and free to use commercially.

**Q: Which model should I use?**
A: Start with `llama3.1:8b` for best balance. Use `gemma:2b` if you need faster responses or have limited RAM.

**Q: Is my data private?**
A: Yes! Everything runs locally on your computer. No data is sent to external servers.

**Q: Can I run this on a laptop?**
A: Yes! For laptops with 8GB RAM, use `gemma:2b` or `llama3.2:1b` for better performance.

## 📄 License

This project is open source. Ollama models are open-source and free to use.
