// Ultra-Advanced Kiosk Chatbot Web Interface
class KioskChatbot {
    constructor() {
        this.socket = null;
        this.connected = false;
        this.currentLanguage = 'en';
        this.voiceRecording = false;
        this.settings = {
            voiceOutput: false,
            darkMode: true,
            highContrast: false,
            animations: true
        };
        
        this.init();
    }
    
    init() {
        this.initializeSocket();
        this.setupEventListeners();
        this.loadSettings();
        this.setupKeyboardShortcuts();
    }
    
    initializeSocket() {
        try {
            this.socket = io();
            
            this.socket.on('connect', () => {
                console.log('Connected to server');
                this.connected = true;
                this.updateConnectionStatus('connected', 'Connected');
            });
            
            this.socket.on('disconnect', () => {
                console.log('Disconnected from server');
                this.connected = false;
                this.updateConnectionStatus('disconnected', 'Disconnected');
            });
            
            this.socket.on('connected', (data) => {
                console.log('Chatbot session created:', data.session_id);
                this.displaySystemMessage(`Connected! Features: ${data.features.join(', ')}`, 'success');
                this.updateFeaturesBanner(data.features);
                // Load available models for dropdown
                this.loadAvailableModels();
            });
            
            this.socket.on('bot_response', (data) => {
                this.hideTypingIndicator();
                this.displayBotMessage(data.message, data.metadata, data.timestamp);
                
                if (this.settings.voiceOutput) {
                    this.speakText(data.message);
                }
            });
            
            this.socket.on('system_message', (data) => {
                this.displaySystemMessage(data.message, data.type);
            });
            
            this.socket.on('typing', (data) => {
                if (data.typing) {
                    this.showTypingIndicator();
                } else {
                    this.hideTypingIndicator();
                }
            });
            
            this.socket.on('error', (data) => {
                this.hideTypingIndicator();
                this.displaySystemMessage(data.message, 'error');
            });
            
            this.socket.on('stats_response', (data) => {
                this.displayStats(data);
            });
            
            this.socket.on('language_changed', (data) => {
                this.currentLanguage = data.language.toLowerCase();
                this.displaySystemMessage(data.message, 'success');
                this.closeModal('languageModal');
            });
            
            this.socket.on('session_cleared', (data) => {
                this.clearChatMessages();
                this.displaySystemMessage(data.message, 'success');
            });
            
            this.socket.on('available_models', (data) => {
                console.log('📥 Received available_models event:', data);
                this.populateModelGrid(data.models);
            });
            
            this.socket.on('model_changed', (data) => {
                this.displaySystemMessage(data.message, 'success');
                this.updateCurrentModel(data.model);
                this.closeModal('modelModal');
            });
            
        } catch (error) {
            console.error('Socket initialization error:', error);
            this.updateConnectionStatus('error', 'Connection Error');
        }
    }
    
    setupEventListeners() {
        // Message input and sending
        const messageInput = document.getElementById('messageInput');
        const sendBtn = document.getElementById('sendBtn');
        const voiceBtn = document.getElementById('voiceBtn');
        
        messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        messageInput.addEventListener('input', (e) => {
            this.updateCharCount(e.target.value.length);
            this.toggleSendButton(e.target.value.trim().length > 0);
        });
        
        sendBtn.addEventListener('click', () => this.sendMessage());
        voiceBtn.addEventListener('click', () => this.toggleVoiceRecording());
        
        // Model selector dropdown
        const modelSelect = document.getElementById('modelSelect');
        if (modelSelect) {
            modelSelect.addEventListener('change', (e) => this.switchModel(e.target.value));
            console.log('✅ Model selector dropdown found and listener added');
        }
        
        // Model change button next to microphone (fallback)
        const modelChangeBtn = document.getElementById('modelChangeBtn');
        if (modelChangeBtn) {
            modelChangeBtn.addEventListener('click', () => this.showModelModal());
            console.log('✅ Model change button (next to mic) found and listener added');
        }
        
        // Control buttons - Add all at once with error handling
        const buttons = [
            { id: 'statsBtn', handler: () => this.showStats() },
            { id: 'languageBtn', handler: () => this.openModal('languageModal') },
            { id: 'clearBtn', handler: () => this.clearSession() },
            { id: 'settingsBtn', handler: () => this.openModal('settingsModal') }
        ];
        
        buttons.forEach(({ id, handler }) => {
            const btn = document.getElementById(id);
            if (btn) {
                btn.addEventListener('click', handler);
                console.log(`✅ ${id} button found and listener added`);
            } else {
                console.error(`❌ ${id} button not found in DOM!`);
            }
        });
        
        // Settings
        document.getElementById('voiceOutput').addEventListener('change', (e) => {
            this.settings.voiceOutput = e.target.checked;
            this.saveSettings();
        });
        
        document.getElementById('darkMode').addEventListener('change', (e) => {
            this.settings.darkMode = e.target.checked;
            this.saveSettings();
            this.applyTheme();
        });
        
        document.getElementById('highContrast').addEventListener('change', (e) => {
            this.settings.highContrast = e.target.checked;
            this.saveSettings();
            this.applyTheme();
        });
        
        document.getElementById('animations').addEventListener('change', (e) => {
            this.settings.animations = e.target.checked;
            this.saveSettings();
            this.applyAnimations();
        });
        
        // Modal close on outside click
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('modal')) {
                this.closeModal(e.target.id);
            }
        });
        
        // Auto-scroll on new messages
        const chatMessages = document.getElementById('chatMessages');
        const observer = new MutationObserver(() => {
            chatMessages.scrollTop = chatMessages.scrollHeight;
        });
        observer.observe(chatMessages, { childList: true });
    }
    
    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Ctrl/Cmd + Enter to send message
            if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
                this.sendMessage();
            }
            
            // Escape to close modals
            if (e.key === 'Escape') {
                this.closeAllModals();
            }
            
            // Ctrl/Cmd + K to focus input
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                document.getElementById('messageInput').focus();
            }
            
            // Ctrl/Cmd + L to clear chat
            if ((e.ctrlKey || e.metaKey) && e.key === 'l') {
                e.preventDefault();
                this.clearSession();
            }
        });
    }
    
    sendMessage() {
        const messageInput = document.getElementById('messageInput');
        const message = messageInput.value.trim();
        
        if (!message || !this.connected) {
            return;
        }
        
        // Display user message
        this.displayUserMessage(message);
        
        // Clear input
        messageInput.value = '';
        this.updateCharCount(0);
        this.toggleSendButton(false);
        
        // Send to server
        this.socket.emit('send_message', { message: message });
        
        // Show typing indicator
        this.showTypingIndicator();
    }
    
    displayUserMessage(message) {
        const chatMessages = document.getElementById('chatMessages');
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message message-user';
        
        const timestamp = new Date().toLocaleTimeString();
        
        messageDiv.innerHTML = `
            <div class="message-content">
                ${this.escapeHtml(message)}
                <div class="message-meta">
                    <span class="message-time">${timestamp}</span>
                </div>
            </div>
        `;
        
        chatMessages.appendChild(messageDiv);
        this.removeWelcomeMessage();
    }
    
    displayBotMessage(message, metadata, timestamp) {
        const chatMessages = document.getElementById('chatMessages');
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message message-bot';
        
        const time = new Date(timestamp).toLocaleTimeString();
        let infoBadges = '';
        
        if (metadata.cached) {
            infoBadges += '<span class="info-badge cached">Cached</span>';
        }
        
        if (metadata.response_time > 3) {
            infoBadges += `<span class="info-badge slow">${metadata.response_time}s</span>`;
        }
        
        if (metadata.model_used && metadata.model_used !== 'unknown') {
            infoBadges += `<span class="info-badge">${metadata.model_used}</span>`;
        }
        
        messageDiv.innerHTML = `
            <div class="message-content">
                ${this.formatMessage(message)}
                <div class="message-meta">
                    <span class="message-time">${time}</span>
                    <div class="message-info">
                        ${infoBadges}
                    </div>
                </div>
            </div>
        `;
        
        chatMessages.appendChild(messageDiv);
        this.removeWelcomeMessage();
    }
    
    displaySystemMessage(message, type = 'info') {
        const chatMessages = document.getElementById('chatMessages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `system-message ${type}`;
        messageDiv.textContent = message;
        
        chatMessages.appendChild(messageDiv);
        
        // Auto-remove system messages after 5 seconds
        setTimeout(() => {
            if (messageDiv.parentNode) {
                messageDiv.style.opacity = '0';
                setTimeout(() => messageDiv.remove(), 300);
            }
        }, 5000);
    }
    
    showTypingIndicator() {
        const indicator = document.getElementById('typingIndicator');
        indicator.classList.add('show');
    }
    
    hideTypingIndicator() {
        const indicator = document.getElementById('typingIndicator');
        indicator.classList.remove('show');
    }
    
    removeWelcomeMessage() {
        const welcomeMessage = document.querySelector('.welcome-message');
        if (welcomeMessage) {
            welcomeMessage.style.opacity = '0';
            setTimeout(() => welcomeMessage.remove(), 300);
        }
    }
    
    updateConnectionStatus(status, text) {
        const statusDot = document.getElementById('connectionStatus');
        const statusText = document.getElementById('statusText');
        
        statusDot.className = `status-dot ${status}`;
        statusText.textContent = text;
    }
    
    updateFeaturesBanner(features) {
        const featuresList = document.getElementById('featuresList');
        featuresList.innerHTML = features.map(feature => 
            `<span class="feature-tag">${feature}</span>`
        ).join('');
    }
    
    updateCharCount(count) {
        const charCount = document.getElementById('charCount');
        charCount.textContent = count;
        
        const charCountElement = charCount.parentElement;
        charCountElement.className = 'char-count';
        
        if (count > 400) {
            charCountElement.classList.add('warning');
        }
        if (count > 450) {
            charCountElement.classList.add('error');
        }
    }
    
    toggleSendButton(enabled) {
        const sendBtn = document.getElementById('sendBtn');
        sendBtn.disabled = !enabled || !this.connected;
    }
    
    // Voice functionality
    toggleVoiceRecording() {
        if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
            this.displaySystemMessage('Speech recognition not supported in this browser', 'error');
            return;
        }
        
        const voiceBtn = document.getElementById('voiceBtn');
        
        if (this.voiceRecording) {
            this.stopVoiceRecording();
        } else {
            this.startVoiceRecording();
        }
    }
    
    startVoiceRecording() {
        try {
            const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
            const recognition = new SpeechRecognition();
            
            recognition.lang = this.getVoiceLanguage();
            recognition.interimResults = false;
            recognition.maxAlternatives = 1;
            
            recognition.onstart = () => {
                this.voiceRecording = true;
                const voiceBtn = document.getElementById('voiceBtn');
                voiceBtn.classList.add('recording');
                this.displaySystemMessage('Listening... Speak clearly', 'info');
            };
            
            recognition.onresult = (event) => {
                const transcript = event.results[0][0].transcript;
                document.getElementById('messageInput').value = transcript;
                this.updateCharCount(transcript.length);
                this.toggleSendButton(transcript.length > 0);
                this.displaySystemMessage(`Heard: "${transcript}"`, 'success');
            };
            
            recognition.onerror = (event) => {
                this.displaySystemMessage(`Speech recognition error: ${event.error}`, 'error');
                this.stopVoiceRecording();
            };
            
            recognition.onend = () => {
                this.stopVoiceRecording();
            };
            
            recognition.start();
            this.recognition = recognition;
            
        } catch (error) {
            this.displaySystemMessage('Error starting voice recognition', 'error');
        }
    }
    
    stopVoiceRecording() {
        this.voiceRecording = false;
        const voiceBtn = document.getElementById('voiceBtn');
        voiceBtn.classList.remove('recording');
        
        if (this.recognition) {
            this.recognition.stop();
            this.recognition = null;
        }
    }
    
    speakText(text) {
        if (!this.settings.voiceOutput || !('speechSynthesis' in window)) {
            return;
        }
        
        try {
            // Cancel any ongoing speech
            speechSynthesis.cancel();
            
            const utterance = new SpeechSynthesisUtterance(text);
            utterance.lang = this.getVoiceLanguage();
            utterance.rate = 0.9;
            utterance.pitch = 1;
            utterance.volume = 0.8;
            
            // Find appropriate voice
            const voices = speechSynthesis.getVoices();
            const preferredVoice = voices.find(voice => 
                voice.lang.startsWith(this.currentLanguage)
            );
            if (preferredVoice) {
                utterance.voice = preferredVoice;
            }
            
            speechSynthesis.speak(utterance);
            
        } catch (error) {
            console.error('Text-to-speech error:', error);
        }
    }
    
    getVoiceLanguage() {
        const languageMap = {
            'en': 'en-US',
            'es': 'es-ES',
            'fr': 'fr-FR',
            'de': 'de-DE',
            'it': 'it-IT',
            'pt': 'pt-PT',
            'ru': 'ru-RU',
            'zh': 'zh-CN',
            'ja': 'ja-JP',
            'ko': 'ko-KR',
            'ar': 'ar-SA',
            'hi': 'hi-IN'
        };
        return languageMap[this.currentLanguage] || 'en-US';
    }
    
    // Modal management
    openModal(modalId) {
        const modal = document.getElementById(modalId);
        modal.classList.add('show');
        document.body.style.overflow = 'hidden';
        
        // Focus first focusable element
        const focusable = modal.querySelector('button, input, [tabindex]:not([tabindex="-1"])');
        if (focusable) {
            setTimeout(() => focusable.focus(), 100);
        }
    }
    
    closeModal(modalId) {
        const modal = document.getElementById(modalId);
        modal.classList.remove('show');
        document.body.style.overflow = 'auto';
    }
    
    closeAllModals() {
        const modals = document.querySelectorAll('.modal');
        modals.forEach(modal => {
            modal.classList.remove('show');
        });
        document.body.style.overflow = 'auto';
    }
    
    // Statistics
    showStats() {
        if (this.connected) {
            this.socket.emit('get_stats');
        } else {
            this.displaySystemMessage('Not connected to server', 'error');
        }
    }
    
    displayStats(data) {
        const statsGrid = document.getElementById('statsGrid');
        const session = data.session;
        const performance = data.performance;
        
        const duration = this.formatDuration(session.duration_seconds);
        
        statsGrid.innerHTML = `
            <div class="stat-card">
                <div class="stat-value">${session.questions_count}</div>
                <div class="stat-label">Questions Asked</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${duration}</div>
                <div class="stat-label">Session Duration</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${session.avg_response_time}s</div>
                <div class="stat-label">Avg Response Time</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${session.language}</div>
                <div class="stat-label">Current Language</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${performance.cache_hits}</div>
                <div class="stat-label">Cache Hits</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${performance.hit_rate}%</div>
                <div class="stat-label">Cache Hit Rate</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${session.errors_encountered}</div>
                <div class="stat-label">Errors</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${performance.active_sessions}</div>
                <div class="stat-label">Active Sessions</div>
            </div>
        `;
        
        this.openModal('statsModal');
    }
    
    formatDuration(seconds) {
        const hours = Math.floor(seconds / 3600);
        const minutes = Math.floor((seconds % 3600) / 60);
        const secs = seconds % 60;
        
        if (hours > 0) {
            return `${hours}h ${minutes}m`;
        } else if (minutes > 0) {
            return `${minutes}m ${secs}s`;
        } else {
            return `${secs}s`;
        }
    }
    
    // Model Selection
    showModelModal() {
        console.log('🔍 showModelModal called, connected:', this.connected);
        if (this.connected) {
            console.log('📡 Emitting get_available_models event');
            // Force cache clear with timestamp
            this.socket.emit('get_available_models', { 
                cache_bust: Date.now(),
                force_refresh: true 
            });
            this.openModal('modelModal');
        } else {
            console.log('❌ Not connected to server');
            this.displaySystemMessage('Not connected to server', 'error');
        }
    }
    
    // Switch Model via Dropdown
    async switchModel(newModel) {
        if (!newModel) return;
        
        console.log('🔄 Switching to model:', newModel);
        
        // Show loading state
        const modelSelect = document.getElementById('modelSelect');
        const originalText = modelSelect.options[modelSelect.selectedIndex].text;
        
        // Disable dropdown during switch
        modelSelect.disabled = true;
        
        // Update status
        this.updateConnectionStatus('connecting', `Switching to ${newModel}...`);
        this.displaySystemMessage(`🔄 Switching to ${newModel}. This may take a moment...`, 'info');
        
        try {
            const response = await fetch('/api/switch-model', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ model: newModel })
            });
            
            const result = await response.json();
            
            if (response.ok && result.success) {
                // Update UI elements
                document.getElementById('currentModelName').textContent = newModel;
                
                // Update status
                this.updateConnectionStatus('connected', 'Connected');
                this.displaySystemMessage(`✅ Successfully switched to ${newModel}!`, 'success');
                
                console.log('✅ Model switched successfully to:', newModel);
            } else {
                // Revert dropdown to previous selection
                const currentModel = document.getElementById('currentModelName').textContent;
                modelSelect.value = currentModel;
                
                this.displaySystemMessage(`❌ Failed to switch model: ${result.error || 'Unknown error'}`, 'error');
                console.error('❌ Model switch failed:', result.error);
            }
        } catch (error) {
            // Revert dropdown to previous selection
            const currentModel = document.getElementById('currentModelName').textContent;
            modelSelect.value = currentModel;
            
            this.displaySystemMessage(`❌ Error switching model: ${error.message}`, 'error');
            console.error('❌ Model switch error:', error);
        } finally {
            // Re-enable dropdown
            modelSelect.disabled = false;
            
            // Reset connection status if needed
            if (this.connected) {
                this.updateConnectionStatus('connected', 'Connected');
            }
        }
    }

    // Load available models for dropdown
    async loadAvailableModels() {
        try {
            const response = await fetch('/api/models');
            if (response.ok) {
                const data = await response.json();
                this.updateModelDropdown(data.models, data.current_model);
            }
        } catch (error) {
            console.error('Failed to load available models:', error);
        }
    }

    updateModelDropdown(models, currentModel) {
        const modelSelect = document.getElementById('modelSelect');
        if (!modelSelect) return;

        // Clear existing options except the first few defaults
        modelSelect.innerHTML = '';

        // Add available models from server
        models.forEach(model => {
            const option = document.createElement('option');
            option.value = model.name;
            option.textContent = `${model.name} (${model.size})`;
            
            if (model.name === currentModel) {
                option.selected = true;
            }
            
            modelSelect.appendChild(option);
        });

        // Update current model display
        if (currentModel) {
            document.getElementById('currentModelName').textContent = currentModel;
        }
    }

    populateModelGrid(models) {
        console.log('🔧 populateModelGrid called with models:', models);
        const modelGrid = document.getElementById('modelGrid');
        const currentModel = document.getElementById('currentModelName').textContent;
        
        console.log('📍 Current model from UI:', currentModel);
        console.log('📍 ModelGrid element:', modelGrid);
        
        // Clear any cached content first
        modelGrid.innerHTML = '';
        
        // Add a debug header to verify this is running
        const debugHeader = document.createElement('div');
        debugHeader.style.cssText = 'background: #00ff00; color: black; padding: 10px; margin: 5px 0; font-weight: bold; border-radius: 5px; text-align: center;';
        debugHeader.textContent = `✅ CACHE CLEARED: ${models.length} Ollama models detected at ${new Date().toLocaleTimeString()}`;
        modelGrid.appendChild(debugHeader);
        
        // Add the actual models
        const modelsHTML = models.map(model => `
            <div class="model-option ${model.name === currentModel ? 'active' : ''}" 
                 onclick="chatbot.changeModel('${model.name}')">
                <div class="model-name">${model.name}</div>
                <div class="model-description">${model.description}</div>
            </div>
        `).join('');
        
        modelGrid.innerHTML = debugHeader.outerHTML + modelsHTML;
        
        console.log('✅ Model grid populated with', models.length, 'models');
    }
    
    changeModel(modelName) {
        if (this.connected) {
            this.socket.emit('change_model', { model_name: modelName });
        } else {
            this.displaySystemMessage('Not connected to server', 'error');
        }
    }
    
    updateCurrentModel(modelName) {
        document.getElementById('currentModelName').textContent = modelName;
        document.getElementById('currentModelDisplay').textContent = modelName;
    }
    
    // Language change
    changeLanguage(languageCode) {
        if (this.connected) {
            this.socket.emit('change_language', { language: languageCode });
        } else {
            this.displaySystemMessage('Not connected to server', 'error');
        }
    }
    
    // Session management
    clearSession() {
        if (confirm('Are you sure you want to clear the current conversation?')) {
            if (this.connected) {
                this.socket.emit('clear_session');
            } else {
                this.clearChatMessages();
                this.displaySystemMessage('Chat cleared locally', 'info');
            }
        }
    }
    
    clearChatMessages() {
        const chatMessages = document.getElementById('chatMessages');
        chatMessages.innerHTML = `
            <div class="welcome-message">
                <div class="welcome-icon">
                    <i class="fas fa-rocket"></i>
                </div>
                <h2>Welcome to Ultra-Advanced Kiosk!</h2>
                <p>Enterprise-grade AI-powered information system with multi-language support, accessibility features, and advanced analytics.</p>
                <div class="quick-commands">
                    <span class="command-label">Quick Commands:</span>
                    <button class="quick-cmd" onclick="sendQuickCommand('help')">Help</button>
                    <button class="quick-cmd" onclick="sendQuickCommand('stats')">Statistics</button>
                    <button class="quick-cmd" onclick="sendQuickCommand('health')">System Health</button>
                </div>
            </div>
        `;
    }
    
    // Settings management
    loadSettings() {
        const saved = localStorage.getItem('kioskSettings');
        if (saved) {
            this.settings = { ...this.settings, ...JSON.parse(saved) };
        }
        
        // Apply settings to UI
        document.getElementById('voiceOutput').checked = this.settings.voiceOutput;
        document.getElementById('darkMode').checked = this.settings.darkMode;
        document.getElementById('highContrast').checked = this.settings.highContrast;
        document.getElementById('animations').checked = this.settings.animations;
        
        this.applyTheme();
        this.applyAnimations();
    }
    
    saveSettings() {
        localStorage.setItem('kioskSettings', JSON.stringify(this.settings));
    }
    
    applyTheme() {
        const body = document.body;
        
        if (this.settings.highContrast) {
            body.classList.add('high-contrast');
        } else {
            body.classList.remove('high-contrast');
        }
        
        // Dark mode is default, so no additional changes needed
    }
    
    applyAnimations() {
        const body = document.body;
        
        if (!this.settings.animations) {
            body.style.setProperty('--transition-fast', '0s');
            body.style.setProperty('--transition-normal', '0s');
            body.style.setProperty('--transition-slow', '0s');
        } else {
            body.style.setProperty('--transition-fast', '0.15s ease');
            body.style.setProperty('--transition-normal', '0.3s ease');
            body.style.setProperty('--transition-slow', '0.5s ease');
        }
    }
    
    // Utility functions
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
    
    formatMessage(message) {
        // Simple markdown-like formatting
        return message
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/\*(.*?)\*/g, '<em>$1</em>')
            .replace(/`(.*?)`/g, '<code>$1</code>')
            .replace(/\n/g, '<br>');
    }
}

// Global functions for HTML event handlers
function sendQuickCommand(command) {
    const messageInput = document.getElementById('messageInput');
    messageInput.value = command;
    chatbot.sendMessage();
}

function changeLanguage(langCode) {
    chatbot.changeLanguage(langCode);
}

function closeModal(modalId) {
    chatbot.closeModal(modalId);
}

function showModelModal() {
    chatbot.showModelModal();
}

// Initialize chatbot when DOM is loaded
let chatbot;
document.addEventListener('DOMContentLoaded', () => {
    chatbot = new KioskChatbot();
    
    // Make sure voices are loaded for text-to-speech
    if ('speechSynthesis' in window) {
        speechSynthesis.onvoiceschanged = () => {
            console.log('Speech synthesis voices loaded');
        };
    }
});

// Handle page visibility changes to manage connections
document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
        // Page is hidden, could pause some activities
    } else {
        // Page is visible, ensure connection is active
        if (chatbot && !chatbot.connected) {
            console.log('Page visible, attempting to reconnect...');
            chatbot.initializeSocket();
        }
    }
});

// Handle online/offline events
window.addEventListener('online', () => {
    chatbot.displaySystemMessage('Connection restored', 'success');
});

window.addEventListener('offline', () => {
    chatbot.displaySystemMessage('Connection lost', 'error');
});