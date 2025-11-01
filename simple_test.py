#!/usr/bin/env python3

"""
🪶 Lightweight Model Tester
============================
Quick test for lightweight Ollama models
"""

import asyncio
import time
import subprocess
import sys

def check_ollama():
    """Check if Ollama is running and accessible"""
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, timeout=10)
        return result.returncode == 0
    except:
        return False

def get_available_models():
    """Get list of available Ollama models"""
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')[1:]  # Skip header
            models = []
            for line in lines:
                if line.strip():
                    model_name = line.split()[0]
                    models.append(model_name)
            return models
        return []
    except:
        return []

async def test_simple_response(model_name):
    """Test a model with a simple prompt"""
    try:
        # Import here to avoid issues if main.py has problems
        from main import UltraAdvancedKioskChatbot, KioskConfig, ModelProvider
        
        config = KioskConfig(
            primary_model_provider=ModelProvider.OLLAMA,
            primary_model_name=model_name,
            fallback_models=[],
            use_rich_ui=False,
            enable_voice=False,
            enable_analytics=False,
            temperature=0.7,
            response_timeout=45
        )
        
        chatbot = UltraAdvancedKioskChatbot(config)
        
        # Simple test prompt
        prompt = "Say hello and tell me your model name in one sentence."
        
        print(f"🔸 Testing {model_name}...")
        start_time = time.time()
        
        response = await chatbot.get_response(prompt)
        
        end_time = time.time()
        response_time = end_time - start_time
        
        print(f"✅ {model_name} ({response_time:.1f}s):")
        print(f"   📝 {response[:80]}{'...' if len(response) > 80 else ''}")
        
        return True, response_time, response
        
    except Exception as e:
        print(f"❌ {model_name}: {str(e)}")
        return False, 0, str(e)

def main():
    """Main testing function"""
    print("🪶 Lightweight Ollama Model Tester")
    print("="*50)
    
    # Check if Ollama is running
    if not check_ollama():
        print("❌ Ollama is not running or not installed!")
        print("💡 Please start Ollama first: ollama serve")
        sys.exit(1)
    
    print("✅ Ollama is running!")
    
    # Get available models
    available_models = get_available_models()
    
    if not available_models:
        print("❌ No models found!")
        print("💡 Please pull some lightweight models:")
        print("   ollama pull gemma:2b")
        print("   ollama pull phi3:mini")
        sys.exit(1)
    
    print(f"📋 Found {len(available_models)} models:")
    for model in available_models:
        print(f"   • {model}")
    
    # Test lightweight models if available
    lightweight_models = ['gemma:2b', 'phi3:mini', 'llama3.2:1b', 'gemma:7b']
    models_to_test = [m for m in lightweight_models if m in available_models]
    
    if not models_to_test:
        print("\n⚠️  No lightweight models found!")
        print("Available models:", available_models)
        
        # Ask user if they want to test available models
        print("\n❓ Test available models instead? (y/N):", end=" ")
        try:
            choice = input().strip().lower()
            if choice == 'y':
                models_to_test = available_models[:3]  # Test first 3
            else:
                sys.exit(0)
        except KeyboardInterrupt:
            sys.exit(0)
    
    print(f"\n🧪 Testing {len(models_to_test)} models...")
    
    # Run tests
    results = []
    for model in models_to_test:
        try:
            success, response_time, response = asyncio.run(test_simple_response(model))
            results.append({
                'model': model,
                'success': success,
                'time': response_time,
                'response': response
            })
        except KeyboardInterrupt:
            print("\n⏹️  Testing interrupted by user")
            break
        except Exception as e:
            print(f"❌ Error testing {model}: {e}")
            results.append({
                'model': model,
                'success': False,
                'time': 0,
                'response': str(e)
            })
    
    # Summary
    print("\n" + "="*50)
    print("📊 RESULTS SUMMARY")
    print("="*50)
    
    successful_models = [r for r in results if r['success']]
    
    if successful_models:
        # Sort by response time
        successful_models.sort(key=lambda x: x['time'])
        
        print("✅ Working models (fastest first):")
        for result in successful_models:
            print(f"   🚀 {result['model']:15} {result['time']:5.1f}s")
        
        fastest = successful_models[0]
        print(f"\n🎯 RECOMMENDATION: Use {fastest['model']} ({fastest['time']:.1f}s)")
        print(f"📝 Update web_app.py primary_model_name to: '{fastest['model']}'")
        
    else:
        print("❌ No models are working properly!")
        print("💡 Try pulling a lightweight model: ollama pull gemma:2b")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
        sys.exit(0)