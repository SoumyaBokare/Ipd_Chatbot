"""
🥧 RASPBERRY PI KIOSK CONFIGURATION
===================================
Optimized configuration for Raspberry Pi 4B with 3.5-inch display
"""

from main import KioskConfig, ModelProvider, LogLevel

def get_pi_optimized_config():
    """Get optimized configuration for Raspberry Pi with Ollama"""
    return KioskConfig(
        # Use Ollama for local AI models
        primary_model_provider=ModelProvider.OLLAMA,
        primary_model_name="llama3.1:8b",  # Your current model
        
        # Ollama fallback options (lighter models)
        fallback_models=[
            (ModelProvider.OLLAMA, "phi3:mini"),  # Lightweight fallback
            (ModelProvider.OLLAMA, "gemma:2b"),   # Ultra-light fallback
        ],
        
        # UI optimizations for small screen
        use_rich_ui=False,  # Simpler UI for better performance
        terminal_width=80,  # Fit 3.5" screen
        
        # Disable resource-intensive features
        enable_voice=False,  # Can cause audio issues on Pi
        enable_caching=True,  # Keep caching for performance
        enable_analytics=False,  # Reduce I/O operations
        
        # Performance optimizations
        max_conversation_turns=20,  # Reduce memory usage
        response_timeout=30,  # Longer timeout for slower CPU
        temperature=0.3,
        
        # Accessibility (important for kiosk)
        enable_accessibility=True,
        
        # Logging
        log_level=LogLevel.INFO,
        
        # Security
        enable_input_validation=True,
        max_input_length=500,  # Limit input size
    )

# Display configuration for 3.5-inch screen
DISPLAY_CONFIG = {
    "width": 480,      # Typical 3.5" display width
    "height": 320,     # Typical 3.5" display height
    "dpi": 150,        # Adjust based on your display
    "orientation": "landscape",  # or "portrait" based on your setup
    "touch_enabled": True,
    "font_size": 14,   # Readable on small screen
    "button_size": 44, # Touch-friendly button size
}

# Web server configuration for Pi
WEB_CONFIG = {
    "host": "0.0.0.0",  # Allow external connections
    "port": 5000,
    "debug": False,     # Disable debug for performance
    "threaded": True,   # Enable threading
    "processes": 1,     # Single process to save memory
}

# Browser configuration for kiosk mode
BROWSER_CONFIG = {
    "fullscreen": True,
    "hide_cursor": True,
    "disable_zoom": True,
    "disable_scrolling": True,
    "auto_refresh": False,
}