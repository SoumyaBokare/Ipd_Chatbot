"""
🛠️ AI MODEL SETUP SCRIPT
========================
This script helps you install dependencies for different AI model providers.
Run this script to set up only the providers you plan to use.
"""

import subprocess
import sys
import os
from typing import List, Dict

def install_package(package: str) -> bool:
    """Install a Python package using pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        return False

def check_package(package: str) -> bool:
    """Check if a package is already installed"""
    try:
        __import__(package)
        return True
    except ImportError:
        return False

# Define package groups for each provider
PROVIDER_PACKAGES: Dict[str, List[str]] = {
    "core": [
        "flask>=2.3.0",
        "flask-socketio>=5.3.0", 
        "rich>=13.0.0",
        "colorama>=0.4.6",
        "langchain-core>=0.2.0",
        "langchain-community>=0.2.0",
        "deep-translator>=1.11.0"
    ],
    
    "ollama": [
        "langchain-ollama>=0.1.0"
    ],
    
    "openai": [
        "langchain-openai>=0.1.0",
        "openai>=1.0.0"
    ],
    
    "anthropic": [
        "langchain-anthropic>=0.1.0",
        "anthropic>=0.25.0"
    ],
    
    "local": [
        "transformers>=4.30.0",
        "torch>=2.0.0"
    ],
    
    "huggingface": [
        "langchain-huggingface>=0.0.3",
        "huggingface_hub>=0.16.0"
    ],
    
    "cohere": [
        "langchain-cohere>=0.1.0",
        "cohere>=4.0.0"
    ],
    
    "google": [
        "langchain-google-genai>=1.0.0",
        "google-generativeai>=0.3.0"
    ],
    
    "mistral": [
        "langchain-mistralai>=0.1.0",
        "mistralai>=0.4.0"
    ],
    
    "replicate": [
        "replicate>=0.15.0"
    ],
    
    "voice": [
        "SpeechRecognition>=3.10.0",
        "pyttsx3>=2.90"
    ],
    
    "optional": [
        "googletrans==4.0.0rc1",
        "pyaudio>=0.2.11"
    ]
}

def main():
    print("🤖 AI Model Provider Setup")
    print("=" * 40)
    print()
    
    # Show available providers
    providers = list(PROVIDER_PACKAGES.keys())
    
    print("Available providers:")
    for i, provider in enumerate(providers, 1):
        package_count = len(PROVIDER_PACKAGES[provider])
        print(f"  {i:2d}. {provider:12s} ({package_count} packages)")
    
    print("\nSpecial options:")
    print(f"  {len(providers)+1:2d}. all          (install everything)")
    print(f"  {len(providers)+2:2d}. minimal      (core + ollama only)")
    print(f"  {len(providers)+3:2d}. cloud        (core + openai + anthropic)")
    print(f"   0. exit")
    
    print()
    
    while True:
        try:
            choice = input("Select providers to install (comma-separated numbers): ").strip()
            
            if choice == "0":
                break
                
            # Parse selection
            selected_numbers = [int(x.strip()) for x in choice.split(",")]
            selected_providers = []
            
            for num in selected_numbers:
                if num == len(providers) + 1:  # all
                    selected_providers = providers
                    break
                elif num == len(providers) + 2:  # minimal
                    selected_providers = ["core", "ollama"]
                    break
                elif num == len(providers) + 3:  # cloud
                    selected_providers = ["core", "openai", "anthropic"]
                    break
                elif 1 <= num <= len(providers):
                    selected_providers.append(providers[num-1])
                else:
                    print(f"Invalid choice: {num}")
                    continue
            
            # Remove duplicates while preserving order
            selected_providers = list(dict.fromkeys(selected_providers))
            
            if not selected_providers:
                print("No providers selected.")
                continue
            
            print(f"\nSelected providers: {', '.join(selected_providers)}")
            
            # Collect all packages to install
            all_packages = []
            for provider in selected_providers:
                all_packages.extend(PROVIDER_PACKAGES[provider])
            
            # Remove duplicates while preserving order
            all_packages = list(dict.fromkeys(all_packages))
            
            print(f"Total packages to install: {len(all_packages)}")
            
            confirm = input("Proceed with installation? (y/N): ").strip().lower()
            if confirm not in ['y', 'yes']:
                continue
            
            # Install packages
            print("\n🔧 Installing packages...")
            success_count = 0
            failed_packages = []
            
            for package in all_packages:
                print(f"Installing {package}...", end=" ")
                if install_package(package):
                    print("✅ SUCCESS")
                    success_count += 1
                else:
                    print("❌ FAILED")
                    failed_packages.append(package)
            
            print(f"\n📊 Installation Summary:")
            print(f"  ✅ Successful: {success_count}/{len(all_packages)}")
            if failed_packages:
                print(f"  ❌ Failed: {len(failed_packages)}")
                print("  Failed packages:")
                for pkg in failed_packages:
                    print(f"    - {pkg}")
            
            # Show environment variable setup
            if any(p in selected_providers for p in ["openai", "anthropic", "huggingface", "cohere", "google", "mistral", "replicate"]):
                print("\n🔑 API KEYS SETUP REQUIRED:")
                print("You need to add API keys for the cloud providers you selected.")
                print("\n📄 RECOMMENDED: Create a .env file")
                print("1. Copy the example: copy .env.example .env")
                print("2. Edit .env with your real API keys")
                print("3. See API_KEYS_SETUP.md for detailed instructions")
                
                print("\n🔗 Get API keys from:")
                key_sources = {
                    "openai": "https://platform.openai.com/ (API Keys section)",
                    "anthropic": "https://console.anthropic.com/ (API Keys section)", 
                    "huggingface": "https://huggingface.co/ (Settings → Access Tokens)",
                    "cohere": "https://dashboard.cohere.ai/ (API Keys section)",
                    "google": "https://makersuite.google.com/app/apikey",
                    "mistral": "https://console.mistral.ai/ (API Keys section)",
                    "replicate": "https://replicate.com/ (Account → API tokens)"
                }
                
                for provider in selected_providers:
                    if provider in key_sources:
                        print(f"  • {provider.upper()}: {key_sources[provider]}")
                
                print("\n🆓 FREE OPTIONS (no API keys needed):")
                if "core" in selected_providers or "ollama" in selected_providers:
                    print("  • Ollama: ollama serve && ollama pull neural-chat")
                if "local" in selected_providers:
                    print("  • LOCAL models: Work offline, no API keys")
            
            print("\n✨ Setup complete!")
            print("📖 Next steps:")
            print("  1. Set up API keys (see API_KEYS_SETUP.md)")
            print("  2. Test models: python test_models.py")
            print("  3. Check examples: python model_config_examples.py")
            break
            
        except ValueError:
            print("Invalid input. Please enter comma-separated numbers.")
        except KeyboardInterrupt:
            print("\n\nSetup cancelled.")
            break

if __name__ == "__main__":
    main()