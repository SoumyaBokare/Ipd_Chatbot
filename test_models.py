"""
🧪 AI MODEL TESTING SCRIPT
==========================
Test different AI model providers to ensure they're working correctly.
"""

import asyncio
import os
from main import MultiModelAIManager, KioskConfig, ModelProvider, LogLevel

async def test_model(provider: ModelProvider, model_name: str, test_prompt: str = "Hello, how are you?"):
    """Test a specific model provider and model"""
    print(f"\n🧪 Testing {provider.value} - {model_name}")
    print("-" * 50)
    
    try:
        # Create configuration for this specific model
        config = KioskConfig(
            primary_model_provider=provider,
            primary_model_name=model_name,
            fallback_models=[],  # No fallbacks for testing
            max_tokens=50,
            temperature=0.3,
            log_level=LogLevel.INFO
        )
        
        # Initialize model manager
        model_manager = MultiModelAIManager(config)
        
        print(f"✅ Model initialized successfully")
        
        # Test response generation
        response, model_used = await model_manager.get_response(test_prompt)
        
        print(f"📝 Prompt: {test_prompt}")
        print(f"🤖 Response: {response[:200]}{'...' if len(response) > 200 else ''}")
        print(f"🏷️  Model used: {model_used}")
        print(f"✅ Test PASSED")
        
        return True
        
    except Exception as e:
        print(f"❌ Test FAILED: {str(e)}")
        return False

async def main():
    print("🤖 AI Model Provider Testing Suite")
    print("=" * 50)
    
    test_cases = [
        # (Provider, Model, Available Check)
        (ModelProvider.OLLAMA, "neural-chat", "Always available if Ollama is running"),
        (ModelProvider.LOCAL, "gpt2", "Requires transformers package"),
        (ModelProvider.LOCAL, "microsoft/DialoGPT-medium", "Requires transformers package"),
        (ModelProvider.OPENAI, "gpt-3.5-turbo", "Requires OPENAI_API_KEY"),
        (ModelProvider.ANTHROPIC, "claude-3-haiku-20240307", "Requires ANTHROPIC_API_KEY"),
        (ModelProvider.HUGGINGFACE, "microsoft/DialoGPT-large", "Requires HUGGINGFACE_API_TOKEN"),
        (ModelProvider.COHERE, "command-light", "Requires COHERE_API_KEY"),
        (ModelProvider.PALM, "gemini-1.5-flash", "Requires GOOGLE_API_KEY"),
        (ModelProvider.MISTRAL, "mistral-small-latest", "Requires MISTRAL_API_KEY"),
        (ModelProvider.REPLICATE, "meta/llama-2-7b-chat", "Requires REPLICATE_API_TOKEN"),
    ]
    
    results = {}
    
    for provider, model_name, requirement in test_cases:
        print(f"\n📋 {provider.value.upper()} - {model_name}")
        print(f"   Requirement: {requirement}")
        
        # Check if required environment variables are set
        required_keys = {
            ModelProvider.OPENAI: "OPENAI_API_KEY",
            ModelProvider.ANTHROPIC: "ANTHROPIC_API_KEY", 
            ModelProvider.HUGGINGFACE: "HUGGINGFACE_API_TOKEN",
            ModelProvider.COHERE: "COHERE_API_KEY",
            ModelProvider.PALM: "GOOGLE_API_KEY",
            ModelProvider.MISTRAL: "MISTRAL_API_KEY",
            ModelProvider.REPLICATE: "REPLICATE_API_TOKEN"
        }
        
        if provider in required_keys:
            if not os.getenv(required_keys[provider]):
                print(f"   ⏭️  Skipped - Missing {required_keys[provider]} environment variable")
                results[f"{provider.value}-{model_name}"] = "skipped"
                continue
        
        # Run the test
        success = await test_model(provider, model_name)
        results[f"{provider.value}-{model_name}"] = "passed" if success else "failed"
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for result in results.values() if result == "passed")
    failed = sum(1 for result in results.values() if result == "failed") 
    skipped = sum(1 for result in results.values() if result == "skipped")
    
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"⏭️  Skipped: {skipped}")
    print(f"📊 Total: {len(results)}")
    
    if failed == 0:
        print("\n🎉 All available models are working correctly!")
    else:
        print(f"\n⚠️  {failed} model(s) failed. Check the errors above.")
    
    # Show recommendations
    print("\n💡 RECOMMENDATIONS:")
    print("1. Start with Ollama models for local testing")
    print("2. Use OpenAI GPT-3.5-turbo for reliable cloud AI")
    print("3. Try LOCAL models for fully offline operation")
    print("4. Set up API keys in .env file for cloud providers")

if __name__ == "__main__":
    asyncio.run(main())