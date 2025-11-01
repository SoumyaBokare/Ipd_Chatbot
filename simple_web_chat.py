"""
🌐 SIMPLE OPENAI WEB CHATBOT
============================
Simplified Flask web application using only OpenAI models.
"""

from flask import Flask, render_template, request, jsonify, session as flask_session
from flask_socketio import SocketIO, emit
import asyncio
import json
import uuid
import threading
from datetime import datetime
import os

# Import the chatbot system
from main import UltraAdvancedKioskChatbot, KioskConfig, ModelProvider, LogLevel

app = Flask(__name__)
app.config['SECRET_KEY'] = 'simple-openai-chatbot-2024'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Global chatbot instance
chatbot = None

def initialize_simple_chatbot():
    """Initialize the OpenAI-only chatbot"""
    global chatbot
    try:
        # Simple OpenAI-only configuration
        config = KioskConfig(
            primary_model_provider=ModelProvider.OPENAI,
            primary_model_name="gpt-3.5-turbo",
            fallback_models=[
                (ModelProvider.OPENAI, "gpt-4o-mini"),
                (ModelProvider.OPENAI, "gpt-4")
            ],
            use_rich_ui=False,
            enable_voice=False,
            enable_accessibility=True,
            enable_analytics=False,  # Simplified - no analytics
            max_tokens=300,
            temperature=0.7,
            timeout=30.0
        )
        
        chatbot = UltraAdvancedKioskChatbot(config)
        print("✅ OpenAI Chatbot initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to initialize chatbot: {e}")
        print("🔧 Make sure your OPENAI_API_KEY is set in .env file")
        return False

@app.route('/')
def index():
    """Main chatbot interface"""
    return render_template('simple_chat.html')

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'chatbot_ready': chatbot is not None,
        'model': 'OpenAI GPT',
        'timestamp': datetime.now().isoformat()
    })

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    session_id = str(uuid.uuid4())
    flask_session['session_id'] = session_id
    
    emit('connected', {
        'session_id': session_id,
        'message': 'Connected to OpenAI Chatbot',
        'model': 'OpenAI GPT-3.5-turbo'
    })
    print(f"🔌 Client connected: {session_id}")

@socketio.on('send_message')
def handle_message(data):
    """Handle incoming messages from clients"""
    try:
        session_id = flask_session.get('session_id')
        message = data.get('message', '').strip()
        
        if not message:
            emit('error', {'message': 'Empty message received'})
            return
        
        print(f"💬 Message from {session_id}: {message}")
        
        # Get response from chatbot
        if chatbot:
            # Show typing indicator
            emit('typing', {'typing': True})
            
            try:
                # Get response synchronously 
                response = chatbot.get_response_sync(message)
                
                # Send response back
                emit('message_response', {
                    'response': response,
                    'model_used': 'OpenAI GPT',
                    'timestamp': datetime.now().isoformat()
                })
                
                print(f"🤖 Response sent to {session_id}")
                
            except Exception as e:
                error_msg = f"Sorry, I encountered an error: {str(e)}"
                emit('message_response', {
                    'response': error_msg,
                    'error': True,
                    'timestamp': datetime.now().isoformat()
                })
                print(f"❌ Error processing message: {e}")
            
            finally:
                emit('typing', {'typing': False})
        else:
            emit('error', {'message': 'Chatbot not initialized'})
            
    except Exception as e:
        print(f"❌ Error in handle_message: {e}")
        emit('error', {'message': 'Internal server error'})

if __name__ == '__main__':
    print("🤖 Simple OpenAI Chatbot Web Server")
    print("=" * 40)
    
    # Initialize chatbot
    if initialize_simple_chatbot():
        print("🚀 Starting web server...")
        print("🌐 Open http://127.0.0.1:5000 in your browser")
        print("🛑 Press Ctrl+C to stop")
        
        try:
            socketio.run(app, host='127.0.0.1', port=5000, debug=False)
        except KeyboardInterrupt:
            print("\n👋 Server stopped")
    else:
        print("\n❌ Failed to start chatbot")
        print("🔧 Check your OpenAI API key setup")