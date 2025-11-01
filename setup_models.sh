#!/bin/bash

# 🚀 Setup Lightweight Ollama Models for Testing
# ============================================

echo "🤖 Setting up lightweight Ollama models for testing..."

# Check if Ollama is installed and running
if ! command -v ollama &> /dev/null; then
    echo "❌ Ollama is not installed. Please install it first:"
    echo "   curl -fsSL https://ollama.ai/install.sh | sh"
    exit 1
fi

# Check if Ollama service is running
if ! ollama list &> /dev/null; then
    echo "❌ Ollama service is not running. Please start it first:"
    echo "   ollama serve"
    exit 1
fi

echo "✅ Ollama is running!"

# Pull lightweight models for testing
echo "📥 Pulling lightweight models (this may take a few minutes)..."

echo "🔹 Pulling Gemma 2B (Primary model - ~1.7GB)"
ollama pull gemma:2b

echo "🔹 Pulling Phi3 Mini (Fallback 1 - ~2.3GB)"
ollama pull phi3:mini

echo "🔹 Pulling Llama 3.2 1B (Fallback 2 - ~1.3GB)"
ollama pull llama3.2:1b

echo "🔹 Pulling Gemma 7B (Fallback 3 - ~5.0GB) - Optional"
read -p "Do you want to pull Gemma 7B as well? (y/N): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    ollama pull gemma:7b
    echo "✅ Gemma 7B pulled successfully"
else
    echo "⏭️  Skipping Gemma 7B (you can pull it later with: ollama pull gemma:7b)"
fi

echo ""
echo "✅ All lightweight models are ready!"
echo ""
echo "📊 Model sizes and performance:"
echo "   • Gemma 2B:     ~1.7GB, Very fast, Good quality"
echo "   • Phi3 Mini:    ~2.3GB, Fast, Great for coding"
echo "   • Llama 3.2 1B: ~1.3GB, Fastest, Basic responses"
echo "   • Gemma 7B:     ~5.0GB, Slower, Best quality"
echo ""
echo "🚀 Now you can run your web app:"
echo "   python3 web_app.py"
echo ""
echo "🔄 To see all available models:"
echo "   ollama list"