"""
🌐 WEB-BASED KIOSK CHATBOT SYSTEM
=====================================
Flask web application for the Ultra-Advanced Kiosk Chatbot
Provides a beautiful HTML/CSS/JavaScript interface for the chatbot.
"""

from flask import Flask, render_template, request, jsonify, session as flask_session
from flask_socketio import SocketIO, emit, disconnect
import asyncio
import json
import uuid
import threading
import subprocess
from datetime import datetime
import os
import sys

# Import the chatbot system
from main import UltraAdvancedKioskChatbot, KioskConfig, ModelProvider, LogLevel, MultiModelAIManager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ultra-advanced-kiosk-2024'
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# Global chatbot instance
chatbot = None
chatbot_lock = threading.Lock()

def initialize_chatbot(model_name="llama3.1:8b"):
    """Initialize the chatbot system with configurable model"""
    global chatbot
    try:
        # Define fallback models (lightweight options)
        fallback_models = [
            (ModelProvider.OLLAMA, "gemma:2b"),     # Fast, lightweight
            (ModelProvider.OLLAMA, "phi3:mini"),    # Good for coding
            (ModelProvider.OLLAMA, "llama3.2:1b"), # Ultra-fast
            (ModelProvider.OLLAMA, "neural-chat")   # Your existing fallback
        ]
        
        # Remove the primary model from fallbacks to avoid duplication
        fallback_models = [fb for fb in fallback_models if fb[1] != model_name]
        
        config = KioskConfig(
            primary_model_provider=ModelProvider.OLLAMA,
            primary_model_name=model_name,  # Configurable model
            fallback_models=fallback_models,
            use_rich_ui=False,  # Disable rich UI for web
            enable_voice=False,  # Disable voice for web to avoid errors
            enable_accessibility=True,
            enable_analytics=True,
            max_conversation_turns=100,
            temperature=0.3
        )
        
        chatbot = UltraAdvancedKioskChatbot(config)
        print("✅ Chatbot initialized successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to initialize chatbot: {e}")
        return False

@app.route('/')
def index():
    """Main chatbot interface"""
    import time
    return render_template('index.html', timestamp=int(time.time()))

@app.route('/api/health')
def health_check():
    """Health check endpoint"""
    current_model = chatbot.config.primary_model_name if chatbot else "None"
    return jsonify({
        'status': 'healthy',
        'chatbot_ready': chatbot is not None,
        'model_provider': 'Ollama',
        'primary_model': current_model,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/models')
def get_available_models():
    """Get list of available Ollama models"""
    try:
        import subprocess
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')[1:]  # Skip header
            models = []
            for line in lines:
                if line.strip():
                    parts = line.split()
                    model_name = parts[0]
                    size = parts[2] if len(parts) > 2 else "Unknown"
                    models.append({
                        'name': model_name,
                        'size': size,
                        'description': get_model_description(model_name)
                    })
            
            return jsonify({
                'models': models,
                'current_model': chatbot.config.primary_model_name if chatbot else None
            })
        else:
            return jsonify({'error': 'Failed to get models'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/switch-model', methods=['POST'])
def switch_model():
    """Switch to a different model"""
    global chatbot
    
    try:
        data = request.get_json()
        new_model = data.get('model')
        
        if not new_model:
            return jsonify({'error': 'No model specified'}), 400
        
        with chatbot_lock:
            print(f"🔄 Switching from {chatbot.config.primary_model_name if chatbot else 'None'} to {new_model}")
            
            # Reinitialize chatbot with new model
            success = initialize_chatbot(new_model)
            
            if success:
                return jsonify({
                    'success': True,
                    'message': f'Successfully switched to {new_model}',
                    'current_model': new_model
                })
            else:
                return jsonify({'error': f'Failed to initialize {new_model}'}), 500
                
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_model_description(model_name):
    """Get friendly description for model"""
    descriptions = {
        'llama3.1:8b': 'Large, high-quality responses (Original)',
        'gemma:2b': 'Lightweight, fast responses',
        'phi3:mini': 'Great for coding and technical questions',
        'llama3.2:1b': 'Ultra-fast, basic responses',
        'neural-chat': 'Conversational, balanced performance',
        'mistral': 'Creative and detailed responses',
        'gemma:7b': 'Medium size, good quality'
    }
    
    for key, desc in descriptions.items():
        if key in model_name:
            return desc
    
    return 'Custom model'

@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    session_id = str(uuid.uuid4())
    flask_session['session_id'] = session_id
    
    with chatbot_lock:
        if chatbot:
            # Create a new chatbot session
            chatbot.create_session()
    
    emit('connected', {
        'session_id': session_id,
        'message': 'Connected to Ultra-Advanced Kiosk System',
        'model': 'Ollama Llama 3.1 8B',
        'features': chatbot._get_enabled_features() if chatbot else []
    })
    print(f"🔌 Client connected: {session_id}")

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    session_id = flask_session.get('session_id')
    if session_id:
        print(f"🔌 Client disconnected: {session_id}")
        
        # Log session if analytics enabled
        with chatbot_lock:
            if chatbot and chatbot.current_session and chatbot.config.enable_analytics:
                try:
                    chatbot.analytics.log_session(chatbot.current_session)
                except Exception as e:
                    print(f"Error logging session: {e}")

@socketio.on('send_message')
def handle_message(data):
    """Handle incoming messages from clients"""
    try:
        user_input = data.get('message', '').strip()
        session_id = flask_session.get('session_id')
        client_sid = request.sid  # Store the client session ID
        
        if not user_input:
            emit('error', {'message': 'Empty message received'})
            return
        
        if not chatbot:
            emit('error', {'message': 'Chatbot not initialized'})
            return
        
        # Emit typing indicator
        emit('typing', {'typing': True})
        
        # Process the message
        def process_message():
            try:
                with chatbot_lock:
                    # Handle special commands
                    command_result = chatbot.handle_special_commands(user_input)
                    
                    if command_result == "exit":
                        socketio.emit('system_message', {
                            'message': 'Session ended. Thank you for using the Ultra-Advanced Kiosk System!',
                            'type': 'success'
                        }, room=client_sid)
                        socketio.emit('disconnect', room=client_sid)
                        return
                    
                    elif command_result in ["cleared", "help_shown", "stats_shown", "language_changed", 
                                          "voice_toggled", "speak_enabled", "accessibility_toggled",
                                          "insights_shown", "health_shown", "cache_shown", "models_shown"]:
                        socketio.emit('system_message', {
                            'message': f'Command executed: {command_result}',
                            'type': 'info'
                        }, room=client_sid)
                        socketio.emit('typing', {'typing': False}, room=client_sid)
                        return
                    
                    # Process regular query asynchronously
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    
                    try:
                        response, metadata = loop.run_until_complete(
                            chatbot.process_query(user_input)
                        )
                        
                        # Send response back to client
                        socketio.emit('bot_response', {
                            'message': response,
                            'metadata': {
                                'response_time': round(metadata['response_time'], 2),
                                'cached': metadata['cached'],
                                'model_used': metadata['model_used'],
                                'language': metadata['language']
                            },
                            'timestamp': datetime.now().isoformat()
                        }, room=client_sid)
                        
                    finally:
                        loop.close()
                        socketio.emit('typing', {'typing': False}, room=client_sid)
                        
            except Exception as e:
                print(f"Error processing message: {e}")
                socketio.emit('error', {
                    'message': 'An error occurred processing your request'
                }, room=client_sid)
                socketio.emit('typing', {'typing': False}, room=client_sid)
        
        # Run message processing in a separate thread
        threading.Thread(target=process_message, daemon=True).start()
        
    except Exception as e:
        print(f"Error in handle_message: {e}")
        emit('error', {'message': 'Server error occurred'})

@socketio.on('get_stats')
def handle_get_stats():
    """Handle request for session statistics"""
    try:
        with chatbot_lock:
            if not chatbot or not chatbot.current_session:
                emit('error', {'message': 'No active session'})
                return
            
            session = chatbot.current_session
            session_duration = datetime.now() - session.start_time
            
            # Get cache stats
            cache_stats = chatbot.cache.get_stats()
            
            stats_data = {
                'session': {
                    'duration_seconds': int(session_duration.total_seconds()),
                    'questions_count': session.questions_count,
                    'avg_response_time': round(session.total_response_time / max(1, session.questions_count), 2),
                    'language': session.preferred_language.upper(),
                    'errors_encountered': session.errors_encountered,
                    'voice_enabled': session.voice_enabled,
                    'accessibility_mode': session.accessibility_mode
                },
                'performance': {
                    'total_requests': chatbot.performance_metrics['total_requests'],
                    'cache_hits': cache_stats['total_hits'],
                    'cache_size': cache_stats['size'],
                    'hit_rate': round(cache_stats['hit_rate'] * 100, 1),
                    'active_sessions': len(chatbot.active_sessions)
                }
            }
            
            emit('stats_response', stats_data)
            
    except Exception as e:
        print(f"Error getting stats: {e}")
        emit('error', {'message': 'Error retrieving statistics'})

@socketio.on('change_language')
def handle_change_language(data):
    """Handle language change requests"""
    try:
        language_code = data.get('language', 'en').lower()
        
        with chatbot_lock:
            if chatbot:
                success = chatbot.change_language(language_code)
                if success:
                    emit('language_changed', {
                        'language': language_code.upper(),
                        'message': f'Language changed to {language_code.upper()}'
                    })
                else:
                    emit('error', {'message': f'Unsupported language: {language_code}'})
            else:
                emit('error', {'message': 'Chatbot not available'})
                
    except Exception as e:
        print(f"Error changing language: {e}")
        emit('error', {'message': 'Error changing language'})

@socketio.on('clear_session')
def handle_clear_session():
    """Handle session clearing"""
    try:
        with chatbot_lock:
            if chatbot:
                if chatbot.current_session:
                    old_session_id = chatbot.current_session.id
                    if chatbot.config.enable_analytics:
                        chatbot.analytics.log_session(chatbot.current_session)
                    del chatbot.active_sessions[old_session_id]
                
                chatbot.create_session()
                emit('session_cleared', {'message': 'New session started with fresh conversation'})
            else:
                emit('error', {'message': 'Chatbot not available'})
                
    except Exception as e:
        print(f"Error clearing session: {e}")
        emit('error', {'message': 'Error clearing session'})

@socketio.on('change_model')
def handle_change_model(data):
    """Handle model change requests"""
    try:
        model_name = data.get('model_name', '').strip()
        
        if not model_name:
            emit('error', {'message': 'Invalid model name'})
            return
        
        with chatbot_lock:
            if chatbot:
                try:
                    # Update the config
                    chatbot.config.primary_model_name = model_name
                    chatbot.config.primary_model_provider = ModelProvider.OLLAMA
                    
                    # Reinitialize the AI manager with new model
                    chatbot.ai_manager = MultiModelAIManager(chatbot.config, chatbot.logger)
                    
                    emit('model_changed', {
                        'model': model_name,
                        'message': f'Model changed to {model_name}'
                    })
                    
                    chatbot.logger.log(LogLevel.INFO, "Model changed via web interface", 
                                     new_model=model_name)
                    
                except Exception as e:
                    emit('error', {'message': f'Failed to change model: {str(e)}'})
            else:
                emit('error', {'message': 'Chatbot not available'})
                
    except Exception as e:
        print(f"Error changing model: {e}")
        emit('error', {'message': 'Error changing model'})

@socketio.on('get_available_models')
def handle_get_available_models():
    """Get list of available Ollama models dynamically"""
    try:
        
        # Get actually installed Ollama models
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True)
        installed_models = []
        
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')[1:]  # Skip header
            for line in lines:
                if line.strip():
                    model_name = line.split()[0]  # Get first column (NAME)
                    # Skip embedding models, only include chat models
                    if 'embed' not in model_name.lower():
                        installed_models.append(model_name)
        
        # Create model descriptions for available models only
        model_descriptions = {
            'llama3.1:8b': 'Llama 3.1 8B - Most accurate & relevant answers (4.9 GB)',
            'neural-chat:latest': 'Intel Neural Chat - Good conversations (4.1 GB)',
            'neural-chat': 'Intel Neural Chat - Good conversations',
            'mistral:latest': 'Mistral 7B - Fast and efficient', 
            'mistral': 'Mistral 7B - Fast and efficient',
            'codellama:latest': 'Code Llama - Programming focused',
            'codellama': 'Code Llama - Programming focused',
        }
        
        # Build available models list with only installed models
        available_models = []
        for model in installed_models:
            description = model_descriptions.get(model, f'{model} - Available Ollama model')
            available_models.append({
                'name': model, 
                'description': description
            })
        
        print(f"🔍 Detected {len(installed_models)} available models: {[m for m in installed_models]}")
        
        # Ensure at least one model is available
        if not available_models:
            available_models = [
                {'name': 'llama3.1:8b', 'description': 'Llama 3.1 8B - Default model (may need to be pulled)'}
            ]
        
        emit('available_models', {'models': available_models})
        
    except Exception as e:
        print(f"Error getting available models: {e}")
        emit('error', {'message': 'Error retrieving available models'})

if __name__ == '__main__':
    print("🌐 Starting Ultra-Advanced Kiosk Web Server...")
    
    # Initialize chatbot with original model
    if not initialize_chatbot("llama3.1:8b"):
        print("❌ Failed to initialize chatbot. Exiting.")
        print("🔧 Make sure Ollama is running and models are available:")
        print("   ollama pull llama3.1:8b")
        print("   ollama pull gemma:2b")
        print("   ollama pull phi3:mini")
        sys.exit(1)
    
    print("✅ Web server ready!")
    print("🚀 Access the chatbot at: http://localhost:5000")
    print("🤖 Primary: Ollama Llama 3.1 8B (Original)")
    print("🔄 Fallbacks: Gemma 2B → Phi3 Mini → Llama 3.2 1B → Neural Chat")
    print("⚙️  Use model dropdown in web interface to switch models")
    print("🔧 Press Ctrl+C to stop the server")
    
    # Run the Flask-SocketIO server
    socketio.run(
        app, 
        debug=False,
        host='0.0.0.0', 
        port=5000,
        allow_unsafe_werkzeug=True
    )