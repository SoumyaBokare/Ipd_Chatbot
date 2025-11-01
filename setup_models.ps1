# 🤖 PowerShell Script for Ollama Lightweight Models Setup
# =========================================================
# Windows PowerShell version of the model setup

Write-Host "🤖 Setting up lightweight Ollama models for testing..." -ForegroundColor Cyan

# Check if Ollama is installed
Write-Host "🔍 Checking Ollama installation..." -ForegroundColor Yellow
try {
    $ollamaVersion = ollama --version
    Write-Host "✅ Ollama is installed: $ollamaVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Ollama is not installed!" -ForegroundColor Red
    Write-Host "💡 Please install Ollama from: https://ollama.ai" -ForegroundColor Yellow
    exit 1
}

# Check if Ollama is running
Write-Host "🔍 Checking if Ollama is running..." -ForegroundColor Yellow
try {
    ollama list | Out-Null
    Write-Host "✅ Ollama service is running!" -ForegroundColor Green
} catch {
    Write-Host "❌ Ollama service is not running!" -ForegroundColor Red
    Write-Host "💡 Please start Ollama service first" -ForegroundColor Yellow
    exit 1
}

# Show current models
Write-Host "`n📋 Current models:" -ForegroundColor Cyan
ollama list

# Pull lightweight models
Write-Host "`n📥 Pulling lightweight models (this may take a few minutes)..." -ForegroundColor Cyan

$models = @(
    @{name="gemma:2b"; description="Primary model (~1.7GB)"; size="Small"},
    @{name="phi3:mini"; description="Fallback 1 (~2.3GB)"; size="Small"},
    @{name="llama3.2:1b"; description="Fallback 2 (~1.3GB)"; size="Tiny"},
    @{name="gemma:7b"; description="Fallback 3 (~5.0GB)"; size="Medium"}
)

foreach ($model in $models) {
    Write-Host "`n🔹 Pulling $($model.name) - $($model.description)" -ForegroundColor Yellow
    
    if ($model.name -eq "gemma:7b") {
        $response = Read-Host "Do you want to pull Gemma 7B as well? (5GB) [y/N]"
        if ($response -ne "y" -and $response -ne "Y") {
            Write-Host "⏭️  Skipping Gemma 7B" -ForegroundColor Gray
            continue
        }
    }
    
    try {
        ollama pull $model.name
        Write-Host "✅ $($model.name) pulled successfully" -ForegroundColor Green
    } catch {
        Write-Host "❌ Failed to pull $($model.name): $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host "`n✅ Setup complete!" -ForegroundColor Green
Write-Host "`n📊 Model performance expectations:" -ForegroundColor Cyan
Write-Host "   • Gemma 2B:     ~1.7GB, Very fast, Good quality" -ForegroundColor White
Write-Host "   • Phi3 Mini:    ~2.3GB, Fast, Great for coding" -ForegroundColor White
Write-Host "   • Llama 3.2 1B: ~1.3GB, Fastest, Basic responses" -ForegroundColor White
Write-Host "   • Gemma 7B:     ~5.0GB, Slower, Best quality" -ForegroundColor White

Write-Host "`n🚀 Next steps:" -ForegroundColor Cyan
Write-Host "   1. Test models: python3 simple_test.py" -ForegroundColor White
Write-Host "   2. Run web app: python3 web_app.py" -ForegroundColor White

Write-Host "`n🔄 To see all models: ollama list" -ForegroundColor Gray