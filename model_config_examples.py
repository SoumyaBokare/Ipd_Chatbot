"""
🤖 AI MODEL CONFIGURATION EXAMPLES
=====================================
This file contains configuration examples for all supported AI model providers.
Copy and modify these configurations based on your needs.

Required Environment Variables:
- OPENAI_API_KEY: For OpenAI models
- ANTHROPIC_API_KEY: For Anthropic Claude models  
- HUGGINGFACE_API_TOKEN: For Hugging Face Hub models
- COHERE_API_KEY: For Cohere models
- GOOGLE_API_KEY: For Google PaLM/Gemini models
- MISTRAL_API_KEY: For Mistral AI models
- REPLICATE_API_TOKEN: For Replicate models
"""

from main import KioskConfig, ModelProvider

# ============================================================================
# EXAMPLE CONFIGURATIONS
# ============================================================================

# 1. OLLAMA (Local models via Ollama)
ollama_config = KioskConfig(
    primary_model_provider=ModelProvider.OLLAMA,
    primary_model_name="llama3.2:latest",
    fallback_models=[
        (ModelProvider.OLLAMA, "neural-chat"),
        (ModelProvider.OLLAMA, "codellama"),
        (ModelProvider.LOCAL, "microsoft/DialoGPT-medium")
    ],
    max_tokens=200,
    temperature=0.3
)

# 2. OPENAI (Cloud-based GPT models)
openai_config = KioskConfig(
    primary_model_provider=ModelProvider.OPENAI,
    primary_model_name="gpt-4",
    fallback_models=[
        (ModelProvider.OPENAI, "gpt-3.5-turbo"),
        (ModelProvider.ANTHROPIC, "claude-3-haiku-20240307"),
        (ModelProvider.LOCAL, "microsoft/DialoGPT-medium")
    ],
    max_tokens=300,
    temperature=0.2
)

# 3. ANTHROPIC (Claude models)
anthropic_config = KioskConfig(
    primary_model_provider=ModelProvider.ANTHROPIC,
    primary_model_name="claude-3-5-sonnet-20241022",
    fallback_models=[
        (ModelProvider.ANTHROPIC, "claude-3-haiku-20240307"),
        (ModelProvider.OPENAI, "gpt-3.5-turbo"),
        (ModelProvider.LOCAL, "microsoft/DialoGPT-medium")
    ],
    max_tokens=400,
    temperature=0.1
)

# 4. LOCAL (Hugging Face Transformers - fully offline)
local_config = KioskConfig(
    primary_model_provider=ModelProvider.LOCAL,
    primary_model_name="microsoft/DialoGPT-medium",
    fallback_models=[
        (ModelProvider.LOCAL, "gpt2"),
        (ModelProvider.LOCAL, "distilgpt2"),
        (ModelProvider.HUGGINGFACE, "microsoft/DialoGPT-large")
    ],
    max_tokens=150,
    temperature=0.7
)

# 5. HUGGINGFACE (Hugging Face Hub API)
huggingface_config = KioskConfig(
    primary_model_provider=ModelProvider.HUGGINGFACE,
    primary_model_name="microsoft/DialoGPT-large",
    fallback_models=[
        (ModelProvider.HUGGINGFACE, "microsoft/DialoGPT-medium"),
        (ModelProvider.LOCAL, "microsoft/DialoGPT-medium"),
        (ModelProvider.OPENAI, "gpt-3.5-turbo")
    ],
    max_tokens=200,
    temperature=0.5
)

# 6. COHERE (Cohere Command models)
cohere_config = KioskConfig(
    primary_model_provider=ModelProvider.COHERE,
    primary_model_name="command",
    fallback_models=[
        (ModelProvider.COHERE, "command-light"),
        (ModelProvider.OPENAI, "gpt-3.5-turbo"),
        (ModelProvider.LOCAL, "microsoft/DialoGPT-medium")
    ],
    max_tokens=250,
    temperature=0.3
)

# 7. PALM/GEMINI (Google models)
google_config = KioskConfig(
    primary_model_provider=ModelProvider.PALM,
    primary_model_name="gemini-1.5-flash",
    fallback_models=[
        (ModelProvider.PALM, "gemini-1.5-pro"),
        (ModelProvider.OPENAI, "gpt-3.5-turbo"),
        (ModelProvider.LOCAL, "microsoft/DialoGPT-medium")
    ],
    max_tokens=300,
    temperature=0.2
)

# 8. MISTRAL (Mistral AI models)
mistral_config = KioskConfig(
    primary_model_provider=ModelProvider.MISTRAL,
    primary_model_name="mistral-large-latest",
    fallback_models=[
        (ModelProvider.MISTRAL, "mistral-small-latest"),
        (ModelProvider.OPENAI, "gpt-3.5-turbo"),
        (ModelProvider.LOCAL, "microsoft/DialoGPT-medium")
    ],
    max_tokens=350,
    temperature=0.1
)

# 9. REPLICATE (Various open-source models via Replicate)
replicate_config = KioskConfig(
    primary_model_provider=ModelProvider.REPLICATE,
    primary_model_name="meta/llama-2-70b-chat",
    fallback_models=[
        (ModelProvider.REPLICATE, "meta/llama-2-13b-chat"),
        (ModelProvider.HUGGINGFACE, "microsoft/DialoGPT-large"),
        (ModelProvider.LOCAL, "microsoft/DialoGPT-medium")
    ],
    max_tokens=200,
    temperature=0.4
)

# ============================================================================
# MULTI-PROVIDER HIGH-AVAILABILITY CONFIG
# ============================================================================

# Enterprise configuration with maximum redundancy
enterprise_config = KioskConfig(
    primary_model_provider=ModelProvider.OPENAI,
    primary_model_name="gpt-4",
    fallback_models=[
        (ModelProvider.ANTHROPIC, "claude-3-5-sonnet-20241022"),
        (ModelProvider.MISTRAL, "mistral-large-latest"),
        (ModelProvider.COHERE, "command"),
        (ModelProvider.HUGGINGFACE, "microsoft/DialoGPT-large"),
        (ModelProvider.LOCAL, "microsoft/DialoGPT-medium"),
        (ModelProvider.OLLAMA, "llama3.2:latest")
    ],
    max_tokens=300,
    temperature=0.2
)

# ============================================================================
# BUDGET-FRIENDLY CONFIG
# ============================================================================

# Cost-optimized configuration using mostly free/cheap models
budget_config = KioskConfig(
    primary_model_provider=ModelProvider.LOCAL,
    primary_model_name="microsoft/DialoGPT-medium",
    fallback_models=[
        (ModelProvider.OLLAMA, "neural-chat"),
        (ModelProvider.HUGGINGFACE, "microsoft/DialoGPT-large"),
        (ModelProvider.OPENAI, "gpt-3.5-turbo"),  # Only as last resort
    ],
    max_tokens=150,
    temperature=0.5
)

# ============================================================================
# POPULAR MODEL RECOMMENDATIONS BY PROVIDER
# ============================================================================

RECOMMENDED_MODELS = {
    ModelProvider.OLLAMA: [
        "llama3.2:latest",      # Meta's latest Llama
        "neural-chat",          # Intel's conversational model
        "codellama",           # Code-specialized model
        "mistral:latest",      # Mistral 7B
        "phi3:latest"          # Microsoft's Phi-3
    ],
    
    ModelProvider.OPENAI: [
        "gpt-4o",              # Latest GPT-4 Optimized
        "gpt-4",               # GPT-4 (more expensive but capable)
        "gpt-3.5-turbo",       # Most popular, cost-effective
        "gpt-4-turbo-preview"  # Latest GPT-4 Turbo
    ],
    
    ModelProvider.ANTHROPIC: [
        "claude-3-5-sonnet-20241022",  # Latest Claude 3.5 Sonnet
        "claude-3-opus-20240229",      # Most capable
        "claude-3-sonnet-20240229",    # Balanced
        "claude-3-haiku-20240307"      # Fastest, cheapest
    ],
    
    ModelProvider.LOCAL: [
        "microsoft/DialoGPT-medium",   # Good conversational model
        "microsoft/DialoGPT-large",    # Better but slower
        "gpt2",                        # Classic, very fast
        "distilgpt2",                  # Smaller, faster GPT-2
        "facebook/blenderbot-400M-distill"  # Facebook's chatbot
    ],
    
    ModelProvider.HUGGINGFACE: [
        "microsoft/DialoGPT-large",
        "facebook/blenderbot-1B-distill",
        "microsoft/DialoGPT-medium",
        "HuggingFaceH4/zephyr-7b-beta"
    ],
    
    ModelProvider.COHERE: [
        "command",             # Latest Command model
        "command-light",       # Lighter, faster version
        "command-nightly"      # Experimental features
    ],
    
    ModelProvider.PALM: [
        "gemini-1.5-pro",      # Most capable
        "gemini-1.5-flash",    # Fastest
        "gemini-pro"           # Previous generation
    ],
    
    ModelProvider.MISTRAL: [
        "mistral-large-latest",    # Most capable
        "mistral-medium-latest",   # Balanced
        "mistral-small-latest"     # Fastest, cheapest
    ],
    
    ModelProvider.REPLICATE: [
        "meta/llama-2-70b-chat",
        "meta/llama-2-13b-chat", 
        "meta/llama-2-7b-chat",
        "mistralai/mixtral-8x7b-instruct-v0.1"
    ]
}

# ============================================================================
# USAGE EXAMPLES
# ============================================================================

if __name__ == "__main__":
    print("🤖 AI Model Configuration Examples")
    print("=" * 50)
    
    # Example: How to use different configurations
    configs = {
        "Ollama (Local)": ollama_config,
        "OpenAI (Cloud)": openai_config,
        "Anthropic (Claude)": anthropic_config,
        "Budget-Friendly": budget_config,
        "Enterprise": enterprise_config
    }
    
    for name, config in configs.items():
        print(f"\n{name}:")
        print(f"  Primary: {config.primary_model_provider.value} - {config.primary_model_name}")
        print(f"  Fallbacks: {len(config.fallback_models)} models")
        print(f"  Max Tokens: {config.max_tokens}")
        print(f"  Temperature: {config.temperature}")