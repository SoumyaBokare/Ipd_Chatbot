"""
🥧 RASPBERRY PI WEB APP
========================
Optimized Flask app for Raspberry Pi 4B with 3.5-inch display
"""

from flask import Flask, render_template, request, jsonify, session as flask_session
from flask_socketio import SocketIO, emit, disconnect
import json
import uuid
import threading
from datetime import datetime
import os
import sys

# Import Pi-optimized configuration
from pi_config import get_pi_optimized_config, DISPLAY_CONFIG, WEB_CONFIG, BROWSER_CONFIG

app = Flask(__name__)
app.config['SECRET_KEY'] = 'pi-kiosk-2024'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Lightweight chatbot for Pi
class PiChatbot:
    def __init__(self, config):
        self.config = config
        self.conversation_history = []
        print("🥧 Pi Chatbot initialized")
    
    async def get_response(self, user_input: str, user_id: str = None) -> str:
        """Get response using API-based model (lightweight)"""
        try:
            # Add to conversation history
            self.conversation_history.append({"role": "user", "content": user_input})
            
            # Simple response for demo - replace with your preferred API
            response = f"Pi Kiosk Response to: {user_input}"
            
            # In a real implementation, you would call your chosen API here:
            # - OpenAI API
            # - Anthropic API  
            # - Hugging Face API
            # - Or any other lightweight API
            
            self.conversation_history.append({"role": "assistant", "content": response})
            
            return response
            
        except Exception as e:
            print(f"Error getting response: {e}")
            return "I apologize, but I'm having trouble processing your request right now."

# Global chatbot instance
chatbot = None
chatbot_lock = threading.Lock()

def initialize_chatbot():
    """Initialize the Pi-optimized chatbot"""
    global chatbot
    try:
        config = get_pi_optimized_config()
        chatbot = PiChatbot(config)
        print("✅ Pi Chatbot initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Error initializing chatbot: {e}")
        return False

@app.route('/')
def index():
    """Main page optimized for 3.5-inch display"""
    return render_template('pi_index.html', display_config=DISPLAY_CONFIG)

@app.route('/api/chat', methods=['POST'])
def chat_api():
    """API endpoint for chat messages"""
    try:
        data = request.get_json()
        user_input = data.get('message', '').strip()
        user_id = data.get('user_id', str(uuid.uuid4()))
        
        if not user_input:
            return jsonify({'error': 'No message provided'}), 400
        
        # Get chatbot response
        with chatbot_lock:
            import asyncio
            response = asyncio.run(chatbot.get_response(user_input, user_id))
        
        return jsonify({
            'response': response,
            'user_id': user_id,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"Error in chat API: {e}")
        return jsonify({'error': 'Internal server error'}), 500

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    print(f"Client connected: {request.sid}")
    emit('connected', {'message': 'Connected to Pi Kiosk!'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    print(f"Client disconnected: {request.sid}")

@socketio.on('send_message')
def handle_message(data):
    """Handle incoming chat messages via WebSocket"""
    try:
        user_input = data.get('message', '').strip()
        user_id = data.get('user_id', str(uuid.uuid4()))
        
        if not user_input:
            emit('error', {'message': 'No message provided'})
            return
        
        # Get chatbot response
        with chatbot_lock:
            import asyncio
            response = asyncio.run(chatbot.get_response(user_input, user_id))
        
        # Send response back to client
        emit('bot_response', {
            'response': response,
            'user_id': user_id,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        print(f"Error handling message: {e}")
        emit('error', {'message': 'Error processing your message'})

if __name__ == '__main__':
    print("🥧 Starting Raspberry Pi Kiosk Web Server...")
    print(f"📺 Display: {DISPLAY_CONFIG['width']}x{DISPLAY_CONFIG['height']}")
    
    # Initialize chatbot
    if not initialize_chatbot():
        print("❌ Failed to initialize chatbot. Using basic responses.")
    
    print("✅ Pi Web server ready!")
    print(f"🚀 Access the kiosk at: http://localhost:{WEB_CONFIG['port']}")
    print("🔧 Press Ctrl+C to stop the server")
    
    # Run the Flask-SocketIO server with Pi-optimized settings
    socketio.run(
        app, 
        debug=WEB_CONFIG['debug'],
        host=WEB_CONFIG['host'], 
        port=WEB_CONFIG['port'],
        allow_unsafe_werkzeug=True
    )