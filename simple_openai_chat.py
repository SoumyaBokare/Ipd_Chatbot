"""
🤖 SIMPLE OPENAI-ONLY CHATBOT CONFIGURATION
==========================================
Simplified version using only OpenAI GPT models.
"""

from main import UltraAdvancedKioskChatbot, KioskConfig, ModelProvider, LogLevel

def create_simple_openai_chatbot():
    """Create a chatbot that only uses OpenAI models"""
    
    # Simple configuration - only OpenAI models
    config = KioskConfig(
        # Primary model
        primary_model_provider=ModelProvider.OPENAI,
        primary_model_name="gpt-3.5-turbo",  # Most cost-effective
        
        # Fallback models (all OpenAI)
        fallback_models=[
            (ModelProvider.OPENAI, "gpt-4o-mini"),  # Cheaper alternative
            (ModelProvider.OPENAI, "gpt-4"),        # More powerful but expensive
        ],
        
        # Response settings
        max_tokens=300,
        temperature=0.7,
        timeout=30.0,
        
        # Other settings
        log_level=LogLevel.INFO,
        enable_voice=False,
        enable_translation=True,
        default_language="en"
    )
    
    return UltraAdvancedKioskChatbot(config)

if __name__ == "__main__":
    print("🤖 Starting OpenAI-Only Chatbot...")
    print("=" * 40)
    
    try:
        # Create and start the chatbot
        chatbot = create_simple_openai_chatbot()
        
        print("✅ Chatbot initialized successfully!")
        print("💬 Type 'quit' to exit\n")
        
        # Simple chat loop
        while True:
            try:
                user_input = input("You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'bye']:
                    print("👋 Goodbye!")
                    break
                
                if user_input:
                    response = chatbot.get_response_sync(user_input)
                    print(f"🤖 Bot: {response}\n")
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                
    except Exception as e:
        print(f"❌ Failed to start chatbot: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure your OpenAI API key is set in .env file")
        print("2. Check your internet connection")
        print("3. Verify you have OpenAI credits available")