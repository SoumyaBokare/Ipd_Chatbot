🔑 API KEYS SETUP GUIDE
======================

There are 3 ways to add API keys to your chatbot:

## 📄 Method 1: .env File (Recommended)

1. **Copy the example file:**
   ```powershell
   copy .env.example .env
   ```

2. **Edit the .env file** with your real API keys:
   ```
   OPENAI_API_KEY=sk-1234567890abcdef...
   ANTHROPIC_API_KEY=sk-ant-api03-...
   HUGGINGFACE_API_TOKEN=hf_1234567890abcdef...
   ```

3. **The .env file will be automatically loaded** when you run the chatbot.

## 🖥️ Method 2: System Environment Variables

### Windows PowerShell:
```powershell
# Set for current session only
$env:OPENAI_API_KEY="your_key_here"
$env:ANTHROPIC_API_KEY="your_key_here"

# Set permanently (requires restart)
[Environment]::SetEnvironmentVariable("OPENAI_API_KEY", "your_key_here", "User")
[Environment]::SetEnvironmentVariable("ANTHROPIC_API_KEY", "your_key_here", "User")
```

### Windows Command Prompt:
```cmd
set OPENAI_API_KEY=your_key_here
set ANTHROPIC_API_KEY=your_key_here
```

## ⚡ Method 3: Runtime (Temporary)

Add this to your Python code before running the chatbot:
```python
import os
os.environ["OPENAI_API_KEY"] = "your_key_here"
os.environ["ANTHROPIC_API_KEY"] = "your_key_here"
```

## 🔗 Where to Get API Keys

### 🤖 OpenAI (GPT models)
- Website: https://platform.openai.com/
- Go to: API Keys section
- Cost: Pay per token (~$0.002/1K tokens for GPT-3.5)

### 🎭 Anthropic (Claude models)
- Website: https://console.anthropic.com/
- Go to: API Keys section  
- Cost: Pay per token (~$0.008/1K tokens for Claude-3-Haiku)

### 🤗 Hugging Face
- Website: https://huggingface.co/
- Go to: Settings → Access Tokens
- Cost: Free tier available

### 💬 Cohere
- Website: https://dashboard.cohere.ai/
- Go to: API Keys section
- Cost: Free tier available (1000 requests/month)

### 🔍 Google (PaLM/Gemini)
- Website: https://makersuite.google.com/app/apikey
- Go to: Get API key
- Cost: Free tier available

### 🌟 Mistral AI
- Website: https://console.mistral.ai/
- Go to: API Keys section
- Cost: Pay per token

### 🔄 Replicate
- Website: https://replicate.com/
- Go to: Account → API tokens
- Cost: Pay per second of compute

## ✅ Testing Your Setup

After adding keys, test them:

```powershell
python test_models.py
```

This will show which models are working with your API keys.

## 🚨 Security Tips

1. **Never commit .env files to git**
   ```powershell
   # Add this to .gitignore
   echo ".env" >> .gitignore
   ```

2. **Use different keys for development vs production**

3. **Set spending limits** on your API accounts

4. **Rotate keys regularly**

## 🆓 Free Options

If you don't want to pay for API keys, you can use:

1. **Ollama** (completely free, local)
   ```powershell
   ollama serve
   ollama pull neural-chat
   ```

2. **LOCAL models** (free, requires disk space)
   - No API keys needed
   - Downloads models automatically

3. **Free tiers** of cloud providers:
   - Hugging Face: Free tier
   - Cohere: 1000 requests/month free
   - Google: Free tier available

## 🔧 Troubleshooting

### "API key not found" error:
- Check if .env file exists and has correct format
- Verify environment variable names match exactly
- Restart terminal/application after setting system variables

### "Invalid API key" error:
- Check if key is copied correctly (no extra spaces)
- Verify the key is active on the provider's website
- Some keys have usage restrictions

### Model still not working:
```powershell
# Check if environment variables are loaded
python -c "import os; print('OPENAI_API_KEY:', bool(os.getenv('OPENAI_API_KEY')))"
```

## 📞 Need Help?

1. Run `python test_models.py` to diagnose issues
2. Check the `logs/` folder for detailed error messages  
3. Make sure you have credits/quota on your API accounts