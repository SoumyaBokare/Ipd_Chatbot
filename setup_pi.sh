#!/bin/bash

# 🥧 Raspberry Pi Kiosk Setup Script
# =================================
# Sets up the chatbot kiosk on Raspberry Pi 4B with 3.5-inch display

echo "🥧 Setting up Pi Kiosk Chatbot..."

# Update system
echo "📦 Updating system packages..."
sudo apt update && sudo apt upgrade -y

# Install Python and pip if not already installed
echo "🐍 Installing Python dependencies..."
sudo apt install -y python3 python3-pip python3-venv git

# Install system dependencies for audio (optional)
echo "🔊 Installing audio dependencies (optional)..."
sudo apt install -y alsa-utils pulseaudio portaudio19-dev

# Install display utilities
echo "📺 Installing display utilities..."
sudo apt install -y xinit xorg openbox chromium-browser unclutter

# Create virtual environment
echo "🏠 Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install Ollama
echo "🤖 Installing Ollama..."
curl -fsSL https://ollama.ai/install.sh | sh

# Install Python packages
echo "📚 Installing Python packages..."
pip install --upgrade pip
pip install -r raspberry_pi_requirements.txt

# Pull lightweight Ollama models for Pi
echo "📥 Pulling Ollama models (this may take a while)..."
ollama pull phi3:mini      # Lightweight model (~2.3GB)
ollama pull llama3.1:8b    # Your preferred model (~4.7GB)

# Create directories
echo "📁 Creating directories..."
mkdir -p logs
mkdir -p static/css
mkdir -p static/js

# Set up display configuration (for 3.5-inch displays)
echo "📺 Setting up display configuration..."

# Create X11 config for small display (adjust as needed)
sudo tee /etc/X11/xorg.conf.d/99-pi-display.conf > /dev/null << 'EOF'
Section "Monitor"
    Identifier "default"
    Option "PreferredMode" "480x320"
    Option "TargetRefresh" "60"
EndSection

Section "Screen"
    Identifier "default"
    Monitor "default"
    DefaultDepth 24
    SubSection "Display"
        Depth 24
        Modes "480x320"
    EndSubSection
EndSection
EOF

# Create autostart script for kiosk mode
echo "🚀 Creating kiosk autostart script..."
mkdir -p ~/.config/openbox
cat > ~/.config/openbox/autostart << 'EOF'
# Disable screen saver and power management
xset s off
xset -dpms
xset s noblank

# Hide cursor
unclutter -idle 0.1 -root &

# Start the Pi web app
cd /home/pi/chatbot
source venv/bin/activate
python3 pi_web_app.py &

# Wait for server to start
sleep 5

# Launch browser in kiosk mode
chromium-browser \
    --kiosk \
    --start-fullscreen \
    --window-size=480,320 \
    --window-position=0,0 \
    --no-first-run \
    --disable-features=TranslateUI \
    --disable-infobars \
    --disable-suggestions-service \
    --disable-save-password-bubble \
    --disable-web-security \
    --disable-features=VizDisplayCompositor \
    --user-data-dir=/tmp/chrome-kiosk \
    http://localhost:5000
EOF

# Make autostart executable
chmod +x ~/.config/openbox/autostart

# Create systemd service for auto-start
echo "⚙️ Creating systemd service..."
sudo tee /etc/systemd/system/pi-kiosk.service > /dev/null << EOF
[Unit]
Description=Pi Kiosk Chatbot
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/chatbot
Environment=PATH=/home/pi/chatbot/venv/bin
ExecStart=/home/pi/chatbot/venv/bin/python /home/pi/chatbot/pi_web_app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable the service
sudo systemctl enable pi-kiosk.service

# Create environment file template
echo "📝 Creating environment file template..."
cat > .env.template << 'EOF'
# Ollama Configuration
OLLAMA_HOST=localhost:11434
OLLAMA_MODELS_PATH=/home/pi/.ollama/models

# Display settings
DISPLAY_WIDTH=480
DISPLAY_HEIGHT=320
KIOSK_MODE=true

# Performance settings
MAX_MEMORY_MB=1000
CACHE_SIZE=100
EOF

# Create start script
echo "🎬 Creating start script..."
cat > start_kiosk.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate

echo "🥧 Starting Pi Kiosk Chatbot..."
python3 pi_web_app.py
EOF

chmod +x start_kiosk.sh

# Create stop script
cat > stop_kiosk.sh << 'EOF'
#!/bin/bash
echo "🛑 Stopping Pi Kiosk..."
pkill -f "pi_web_app.py"
pkill -f "chromium-browser"
EOF

chmod +x stop_kiosk.sh

echo ""
echo "✅ Pi Kiosk setup complete!"
echo ""
echo "📋 Next steps:"
echo "1. Copy your chatbot files to /home/pi/chatbot/"
echo "2. Edit .env file with your API keys (copy from .env.template)"
echo "3. Test with: ./start_kiosk.sh"
echo "4. For auto-start on boot: sudo systemctl start pi-kiosk"
echo "5. To enable GUI auto-start, edit /etc/rc.local and add:"
echo "   su pi -c 'startx' &"
echo ""
echo "🔧 Troubleshooting:"
echo "- Check display with: xrandr"
echo "- Test touch: evtest /dev/input/event0"
echo "- View logs: journalctl -u pi-kiosk -f"
echo ""
echo "🌐 Access your kiosk at: http://localhost:5000"