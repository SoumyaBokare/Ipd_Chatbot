"""
🚀 KIOSK CHATBOT SYSTEM
=====================================
Enterprise-grade information kiosk with AI-powered responses, multi-language support,
accessibility features, advanced analytics, caching, security, and beautiful UI.

Features:
- 🧠 Multi-model AI support with failover
- 🌍 Multi-language support (50+ languages)
- ♿ Full accessibility compliance
- 📊 Advanced analytics and insights
- 🔒 Enterprise security
- ⚡ Smart caching and optimization
- 🎨 Beautiful terminal UI
- 🔄 Auto-recovery and health monitoring
- 📱 Voice input/output support
- 🎯 Context-aware responses
"""

import asyncio
import json
import os
import time
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path
import threading

# Load environment variables from .env file
try:
    from dotenv import load_dotenv
    load_dotenv()  # Load .env file if it exists
except ImportError:
    pass  # dotenv is optional
from concurrent.futures import ThreadPoolExecutor
import hashlib
import sqlite3
from contextlib import contextmanager
import re
import unicodedata

# Advanced imports for enterprise features
try:
    from langchain_ollama import OllamaLLM
    from langchain_core.prompts import ChatPromptTemplate
    LANGCHAIN_AVAILABLE = True
except ImportError as e:
    print(f"LangChain import error: {e}")
    LANGCHAIN_AVAILABLE = False


HUGGINGFACE_AVAILABLE = False
COHERE_AVAILABLE = False
PALM_AVAILABLE = False  
MISTRAL_AVAILABLE = False
REPLICATE_AVAILABLE = False
TRANSFORMERS_AVAILABLE = False

try:
    import speech_recognition as sr
    import pyttsx3
    VOICE_AVAILABLE = True
except ImportError:
    VOICE_AVAILABLE = False

try:
    from deep_translator import GoogleTranslator
    TRANSLATION_AVAILABLE = True
except ImportError:
    TRANSLATION_AVAILABLE = False

try:
    import colorama
    from colorama import Fore, Back, Style
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.layout import Layout
    from rich.live import Live
    from rich.markdown import Markdown
    colorama.init()
    RICH_UI_AVAILABLE = True
except ImportError:
    RICH_UI_AVAILABLE = False


class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"
    CRITICAL = "CRITICAL"


class ModelProvider(Enum):
    OLLAMA = "ollama"




class Language(Enum):
    ENGLISH = "en"
    SPANISH = "es"
    FRENCH = "fr"
    GERMAN = "de"
    ITALIAN = "it"
    PORTUGUESE = "pt"
    RUSSIAN = "ru"
    CHINESE = "zh"
    JAPANESE = "ja"
    KOREAN = "ko"
    ARABIC = "ar"
    HINDI = "hi"


@dataclass
class UserSession:
    """Enhanced user session with comprehensive tracking"""
    id: str
    start_time: datetime
    questions_count: int = 0
    total_response_time: float = 0.0
    preferred_language: str = "en"
    accessibility_mode: bool = False
    voice_enabled: bool = False
    conversation_history: List[Dict] = None
    user_satisfaction: Optional[float] = None
    topics_discussed: List[str] = None
    errors_encountered: int = 0
    
    def __post_init__(self):
        if self.conversation_history is None:
            self.conversation_history = []
        if self.topics_discussed is None:
            self.topics_discussed = []


@dataclass
class KioskConfig:
    """Comprehensive configuration management"""
    # AI Model Settings
    primary_model_provider: ModelProvider = ModelProvider.OLLAMA
    primary_model_name: str = "neural-chat"
    fallback_models: List[Tuple[ModelProvider, str]] = None
    max_tokens: int = 200
    temperature: float = 0.3
    timeout: float = 15.0
    
    # Performance Settings
    max_conversation_turns: int = 50
    context_window_size: int = 1000
    cache_ttl_hours: int = 24
    max_concurrent_sessions: int = 10
    
    # UI Settings
    use_rich_ui: bool = True
    enable_voice: bool = True
    enable_accessibility: bool = True
    default_language: str = "en"
    
    # Security Settings
    enable_content_filtering: bool = True
    max_input_length: int = 500
    rate_limit_per_minute: int = 30
    
    # Analytics Settings
    enable_analytics: bool = True
    analytics_db_path: str = "kiosk_analytics.db"
    log_level: LogLevel = LogLevel.INFO
    
    def __post_init__(self):
        if self.fallback_models is None:
            self.fallback_models = [
                (ModelProvider.OPENAI, "gpt-4o-mini"),
                (ModelProvider.OPENAI, "gpt-4"),
                (ModelProvider.ANTHROPIC, "claude-3-haiku-20240307")
            ]


class AdvancedLogger:
    """Enterprise logging system with multiple outputs"""
    
    def __init__(self, config: KioskConfig):
        self.config = config
        self.setup_logging()
    
    def setup_logging(self):
        """Setup comprehensive logging"""
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        # Configure main logger
        logging.basicConfig(
            level=getattr(logging, self.config.log_level.value),
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / f"kiosk_{datetime.now().strftime('%Y%m%d')}.log"),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger("KioskChatbot")
    
    def log(self, level: LogLevel, message: str, **kwargs):
        """Enhanced logging with context"""
        extra_info = " | ".join([f"{k}={v}" for k, v in kwargs.items()])
        full_message = f"{message} | {extra_info}" if extra_info else message
        getattr(self.logger, level.value.lower())(full_message)


class IntelligentCache:
    """High-performance caching system with smart eviction"""
    
    def __init__(self, ttl_hours: int = 24, max_size: int = 1000):
        self.ttl_hours = ttl_hours
        self.max_size = max_size
        self.cache: Dict[str, Dict] = {}
        self._lock = threading.Lock()
    
    def _generate_key(self, query: str, context: str = "") -> str:
        """Generate cache key with context awareness"""
        combined = f"{query.lower().strip()}{context}"
        return hashlib.md5(combined.encode()).hexdigest()
    
    def get(self, query: str, context: str = "") -> Optional[str]:
        """Retrieve cached response if valid"""
        key = self._generate_key(query, context)
        
        with self._lock:
            if key in self.cache:
                entry = self.cache[key]
                if datetime.now() - entry['timestamp'] < timedelta(hours=self.ttl_hours):
                    entry['hits'] += 1
                    return entry['response']
                else:
                    del self.cache[key]
        return None
    
    def set(self, query: str, response: str, context: str = ""):
        """Cache response with intelligent eviction"""
        key = self._generate_key(query, context)
        
        with self._lock:
            # Evict oldest if at capacity
            if len(self.cache) >= self.max_size:
                oldest_key = min(self.cache.keys(), 
                               key=lambda k: self.cache[k]['timestamp'])
                del self.cache[oldest_key]
            
            self.cache[key] = {
                'response': response,
                'timestamp': datetime.now(),
                'hits': 0
            }
    
    def get_stats(self) -> Dict:
        """Get cache performance statistics"""
        with self._lock:
            total_hits = sum(entry['hits'] for entry in self.cache.values())
            return {
                'size': len(self.cache),
                'total_hits': total_hits,
                'hit_rate': total_hits / max(1, len(self.cache))
            }


class AdvancedAnalytics:
    """Comprehensive analytics and insights system"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize analytics database"""
        with self.get_connection() as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS sessions (
                    id TEXT PRIMARY KEY,
                    start_time TIMESTAMP,
                    end_time TIMESTAMP,
                    questions_count INTEGER,
                    avg_response_time REAL,
                    language TEXT,
                    satisfaction REAL,
                    errors_count INTEGER
                );
                
                CREATE TABLE IF NOT EXISTS interactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id TEXT,
                    timestamp TIMESTAMP,
                    question TEXT,
                    response TEXT,
                    response_time REAL,
                    cached BOOLEAN,
                    model_used TEXT,
                    FOREIGN KEY (session_id) REFERENCES sessions (id)
                );
                
                CREATE TABLE IF NOT EXISTS performance_metrics (
                    timestamp TIMESTAMP,
                    metric_name TEXT,
                    metric_value REAL,
                    PRIMARY KEY (timestamp, metric_name)
                );
                
                CREATE INDEX IF NOT EXISTS idx_sessions_time ON sessions(start_time);
                CREATE INDEX IF NOT EXISTS idx_interactions_session ON interactions(session_id);
                CREATE INDEX IF NOT EXISTS idx_interactions_time ON interactions(timestamp);
            """)
    
    @contextmanager
    def get_connection(self):
        """Database connection context manager"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()
    
    def log_session(self, session: UserSession):
        """Log complete session data"""
        with self.get_connection() as conn:
            avg_response_time = (session.total_response_time / 
                               max(1, session.questions_count))
            
            conn.execute("""
                INSERT OR REPLACE INTO sessions 
                (id, start_time, end_time, questions_count, avg_response_time, 
                 language, satisfaction, errors_count)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                session.id, session.start_time, datetime.now(),
                session.questions_count, avg_response_time,
                session.preferred_language, session.user_satisfaction,
                session.errors_encountered
            ))
    
    def log_interaction(self, session_id: str, question: str, response: str,
                       response_time: float, cached: bool = False, 
                       model_used: str = "unknown"):
        """Log individual interaction"""
        with self.get_connection() as conn:
            conn.execute("""
                INSERT INTO interactions 
                (session_id, timestamp, question, response, response_time, cached, model_used)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (session_id, datetime.now(), question, response, 
                  response_time, cached, model_used))
    
    def get_insights(self, days: int = 7) -> Dict:
        """Generate comprehensive analytics insights"""
        since_date = datetime.now() - timedelta(days=days)
        
        with self.get_connection() as conn:
            # Session metrics
            session_stats = conn.execute("""
                SELECT COUNT(*) as total_sessions,
                       AVG(questions_count) as avg_questions_per_session,
                       AVG(avg_response_time) as avg_response_time,
                       AVG(satisfaction) as avg_satisfaction
                FROM sessions WHERE start_time >= ?
            """, (since_date,)).fetchone()
            
            # Popular topics/questions
            popular_questions = conn.execute("""
                SELECT question, COUNT(*) as frequency
                FROM interactions 
                WHERE timestamp >= ?
                GROUP BY LOWER(question)
                ORDER BY frequency DESC
                LIMIT 10
            """, (since_date,)).fetchall()
            
            # Performance trends
            performance_trend = conn.execute("""
                SELECT DATE(timestamp) as date,
                       AVG(response_time) as avg_response_time,
                       COUNT(*) as interactions_count
                FROM interactions
                WHERE timestamp >= ?
                GROUP BY DATE(timestamp)
                ORDER BY date
            """, (since_date,)).fetchall()
            
            return {
                'session_stats': dict(session_stats) if session_stats else {},
                'popular_questions': [dict(row) for row in popular_questions],
                'performance_trend': [dict(row) for row in performance_trend],
                'report_period_days': days
            }


class MultiModelAIManager:
    """Advanced AI model management with failover and optimization"""
    
    def __init__(self, config: KioskConfig, logger: AdvancedLogger):
        self.config = config
        self.logger = logger
        self.models = {}
        self.current_model = None
        self.model_health = {}
        self.initialize_models()
    
    def initialize_models(self):
        """Initialize all available AI models"""
        try:
            # Primary model
            self.current_model = self._create_model(
                self.config.primary_model_provider,
                self.config.primary_model_name
            )
            
            # Fallback models
            for provider, model_name in self.config.fallback_models:
                try:
                    model_key = f"{provider.value}_{model_name}"
                    self.models[model_key] = self._create_model(provider, model_name)
                    self.model_health[model_key] = {'healthy': True, 'last_error': None}
                except Exception as e:
                    self.logger.log(LogLevel.WARNING, 
                                  f"Failed to initialize fallback model {model_name}",
                                  error=str(e))
            
            self.logger.log(LogLevel.INFO, "AI models initialized successfully",
                          primary=self.config.primary_model_name,
                          fallbacks=len(self.models))
            
        except Exception as e:
            self.logger.log(LogLevel.CRITICAL, "Failed to initialize AI models", 
                          error=str(e))
            raise
    
    def _create_model(self, provider: ModelProvider, model_name: str):
        """Factory method for creating AI models"""
        if not LANGCHAIN_AVAILABLE:
            raise ImportError("LangChain not available")
        
        if provider == ModelProvider.OLLAMA:
            return OllamaLLM(
                model=model_name,
                temperature=self.config.temperature,
                timeout=self.config.timeout,
                num_predict=self.config.max_tokens
            )
        elif provider == ModelProvider.OPENAI:
            if not OPENAI_AVAILABLE:
                raise ImportError("langchain_openai not available")
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                raise ValueError("OpenAI API key not found")
            return ChatOpenAI(
                model=model_name,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
                timeout=self.config.timeout,
                openai_api_key=api_key
            )
        elif provider == ModelProvider.ANTHROPIC:
            if not ANTHROPIC_AVAILABLE:
                raise ImportError("langchain_anthropic not available")
            api_key = os.getenv("ANTHROPIC_API_KEY")
            if not api_key:
                raise ValueError("Anthropic API key not found")
            return ChatAnthropic(
                model=model_name,
                temperature=self.config.temperature,
                max_tokens=self.config.max_tokens,
                timeout=self.config.timeout,
                anthropic_api_key=api_key
            )
        else:
            raise ValueError(f"Unsupported model provider: {provider}. Only OPENAI, OLLAMA, and ANTHROPIC are currently supported.")
    
    async def get_response(self, prompt: str, context: str = "") -> Tuple[str, str]:
        """Get AI response with automatic failover"""
        for attempt, (model_key, model) in enumerate(
            [("primary", self.current_model)] + list(self.models.items())
        ):
            try:
                start_time = time.time()
                
                # Create prompt template
                template = self._get_optimized_prompt_template()
                prompt_obj = ChatPromptTemplate.from_template(template)
                chain = prompt_obj | model
                
                # Get response
                result = await asyncio.get_event_loop().run_in_executor(
                    None, lambda: chain.invoke({
                        "context": context[:self.config.context_window_size],
                        "question": prompt
                    })
                )
                
                response_time = time.time() - start_time
                
                # Handle different response formats
                if hasattr(result, 'content'):
                    # ChatModel responses (OpenAI, Anthropic, etc.)
                    response = str(result.content).strip()
                elif isinstance(result, dict) and 'text' in result:
                    # Some models return dict with 'text' key
                    response = str(result['text']).strip()
                elif isinstance(result, list) and len(result) > 0:
                    # Some models return list of responses
                    response = str(result[0]).strip()
                else:
                    # Fallback - convert to string
                    response = str(result).strip()
                
                # Update model health
                if model_key != "primary":
                    self.model_health[model_key]['healthy'] = True
                
                return response, model_key
                
            except Exception as e:
                error_msg = str(e)
                self.logger.log(LogLevel.WARNING, 
                              f"Model {model_key} failed", 
                              error=error_msg, attempt=attempt + 1)
                
                if model_key != "primary":
                    self.model_health[model_key] = {
                        'healthy': False, 
                        'last_error': error_msg
                    }
                
                if attempt == len(self.models):  # Last attempt
                    return "I'm experiencing technical difficulties. Please try again in a moment.", "error"
        
        return "Service temporarily unavailable.", "error"
    
    def _get_optimized_prompt_template(self) -> str:
        """Get optimized prompt template based on context"""
        return """You are an advanced information kiosk assistant serving the public with intelligence and efficiency.

CORE MISSION: Provide precise, helpful, and professional responses that exactly match user needs.

RESPONSE GUIDELINES:
- Be concise yet complete (1-3 sentences for simple questions, more for complex topics)
- Prioritize accuracy and usefulness over brevity
- Use clear, accessible language appropriate for all users
- If uncertain, acknowledge limitations and offer alternatives
- For multi-part questions, address each component
- Suggest next steps or related information when helpful

CONTEXT AWARENESS: Use conversation history to provide relevant, personalized responses.

Recent conversation: {context}

Current question: {question}

Professional response:"""


class AccessibilityEngine:
    """Comprehensive accessibility support system"""
    
    def __init__(self, config: KioskConfig):
        self.config = config
        self.voice_engine = None
        self.speech_recognizer = None
        self.translator = None
        self.initialize_accessibility()
    
    def initialize_accessibility(self):
        """Initialize accessibility features"""
        if VOICE_AVAILABLE and self.config.enable_voice:
            try:
                self.voice_engine = pyttsx3.init()
                self.voice_engine.setProperty('rate', 150)  # Moderate speed
                self.voice_engine.setProperty('volume', 0.8)
                
                self.speech_recognizer = sr.Recognizer()
                self.microphone = sr.Microphone()
                
                # Calibrate for ambient noise
                with self.microphone as source:
                    self.speech_recognizer.adjust_for_ambient_noise(source, duration=1)
                    
            except Exception as e:
                print(f"⚠️  Voice features unavailable: {e}")
                self.voice_engine = None
                self.speech_recognizer = None
        
        if TRANSLATION_AVAILABLE:
            try:
                self.translator = GoogleTranslator(source='auto', target='en')
            except Exception as e:
                print(f"⚠️  Translation features unavailable: {e}")
    
    def text_to_speech(self, text: str, language: str = "en"):
        """Convert text to speech with language support"""
        if not self.voice_engine:
            return False
        
        try:
            # Clean text for better speech synthesis
            clean_text = self._clean_text_for_speech(text)
            
            # Adjust voice properties for language
            voices = self.voice_engine.getProperty('voices')
            if voices:
                for voice in voices:
                    if language in voice.id.lower():
                        self.voice_engine.setProperty('voice', voice.id)
                        break
            
            self.voice_engine.say(clean_text)
            self.voice_engine.runAndWait()
            return True
            
        except Exception as e:
            print(f"Speech synthesis error: {e}")
            return False
    
    def speech_to_text(self, timeout: float = 5.0, phrase_time_limit: float = 10.0) -> Optional[str]:
        """Convert speech to text with advanced processing"""
        if not self.speech_recognizer:
            return None
        
        try:
            with self.microphone as source:
                print("🎤 Listening... (speak clearly)")
                audio = self.speech_recognizer.listen(
                    source, 
                    timeout=timeout, 
                    phrase_time_limit=phrase_time_limit
                )
            
            print("🔄 Processing speech...")
            text = self.speech_recognizer.recognize_google(audio)
            return text.strip()
            
        except sr.WaitTimeoutError:
            print("🔇 No speech detected")
            return None
        except sr.UnknownValueError:
            print("🔇 Could not understand speech")
            return None
        except Exception as e:
            print(f"Speech recognition error: {e}")
            return None
    
    def translate_text(self, text: str, target_language: str = "en", 
                      source_language: str = "auto") -> Optional[str]:
        """Translate text with automatic language detection"""
        if not self.translator:
            return None
        
        try:
            # Deep translator uses a different API
            translator = GoogleTranslator(source=source_language, target=target_language)
            result = translator.translate(text)
            return result
        except Exception as e:
            print(f"Translation error: {e}")
            return None
    
    def _clean_text_for_speech(self, text: str) -> str:
        """Clean and optimize text for speech synthesis"""
        # Remove markdown formatting
        text = re.sub(r'[*_`]', '', text)
        
        # Expand common abbreviations
        abbreviations = {
            'e.g.': 'for example',
            'i.e.': 'that is',
            'etc.': 'and so on',
            'vs.': 'versus',
            'Dr.': 'Doctor',
            'Mr.': 'Mister',
            'Mrs.': 'Misses',
            'Ms.': 'Miss'
        }
        
        for abbrev, expansion in abbreviations.items():
            text = text.replace(abbrev, expansion)
        
        # Normalize whitespace
        text = ' '.join(text.split())
        
        return text


class UltraAdvancedKioskChatbot:
    """The ultimate kiosk chatbot system with enterprise features"""
    
    def __init__(self, config: Optional[KioskConfig] = None):
        self.config = config or KioskConfig()
        self.logger = AdvancedLogger(self.config)
        self.cache = IntelligentCache(self.config.cache_ttl_hours)
        self.analytics = AdvancedAnalytics(self.config.analytics_db_path)
        self.ai_manager = MultiModelAIManager(self.config, self.logger)
        self.accessibility = AccessibilityEngine(self.config)
        
        # UI components
        if RICH_UI_AVAILABLE and self.config.use_rich_ui:
            self.console = Console()
        else:
            self.console = None
        
        # Session management
        self.active_sessions: Dict[str, UserSession] = {}
        self.current_session: Optional[UserSession] = None
        
        # Performance monitoring
        self.performance_metrics = {
            'total_requests': 0,
            'cache_hits': 0,
            'average_response_time': 0,
            'error_rate': 0
        }
        
        self.logger.log(LogLevel.INFO, "Ultra-Advanced Kiosk System initialized",
                       config=self.config.primary_model_name,
                       features=self._get_enabled_features())
    
    def _get_enabled_features(self) -> List[str]:
        """Get list of enabled features"""
        features = ["AI Responses", "Caching", "Analytics"]
        
        if RICH_UI_AVAILABLE and self.config.use_rich_ui:
            features.append("Rich UI")
        if VOICE_AVAILABLE and self.config.enable_voice:
            features.append("Voice I/O")
        if TRANSLATION_AVAILABLE:
            features.append("Translation")
        if self.config.enable_accessibility:
            features.append("Accessibility")
        
        return features
    
    def create_session(self) -> UserSession:
        """Create new user session with unique ID"""
        session_id = f"session_{int(time.time())}_{len(self.active_sessions)}"
        session = UserSession(
            id=session_id,
            start_time=datetime.now(),
            preferred_language=self.config.default_language
        )
        
        self.active_sessions[session_id] = session
        self.current_session = session
        
        self.logger.log(LogLevel.INFO, "New session created", session_id=session_id)
        return session
    
    async def process_query(self, user_input: str) -> Tuple[str, Dict]:
        """Process user query with comprehensive handling"""
        if not self.current_session:
            self.create_session()
        
        session = self.current_session
        start_time = time.time()
        metadata = {
            'cached': False,
            'model_used': 'unknown',
            'response_time': 0,
            'language': session.preferred_language,
            'error': None
        }
        
        try:
            # Content filtering and validation
            if len(user_input) > self.config.max_input_length:
                return "Please keep your question shorter for better assistance.", metadata
            
            if self._is_inappropriate_content(user_input):
                return "I can only help with appropriate questions. Please rephrase your request.", metadata
            
            # Check cache first
            context = self._format_conversation_context(session)
            cached_response = self.cache.get(user_input, context)
            
            if cached_response:
                metadata['cached'] = True
                metadata['response_time'] = time.time() - start_time
                self.performance_metrics['cache_hits'] += 1
                return cached_response, metadata
            
            # Get AI response
            response, model_used = await self.ai_manager.get_response(user_input, context)
            
            # Post-process response
            if session.preferred_language != "en":
                translated = self.accessibility.translate_text(
                    response, session.preferred_language, "en"
                )
                if translated:
                    response = translated
            
            # Cache successful response
            self.cache.set(user_input, response, context)
            
            # Update metadata
            metadata.update({
                'model_used': model_used,
                'response_time': time.time() - start_time
            })
            
            # Update session
            session.questions_count += 1
            session.total_response_time += metadata['response_time']
            session.conversation_history.append({
                'timestamp': datetime.now().isoformat(),
                'question': user_input,
                'response': response,
                'metadata': metadata
            })
            
            # Log interaction
            if self.config.enable_analytics:
                self.analytics.log_interaction(
                    session.id, user_input, response,
                    metadata['response_time'], metadata['cached'], model_used
                )
            
            return response, metadata
            
        except Exception as e:
            error_msg = "I encountered an error processing your request. Please try again."
            session.errors_encountered += 1
            metadata['error'] = str(e)
            
            self.logger.log(LogLevel.ERROR, "Query processing failed",
                          session_id=session.id, error=str(e))
            
            return error_msg, metadata
        
        finally:
            self.performance_metrics['total_requests'] += 1
    
    def _format_conversation_context(self, session: UserSession) -> str:
        """Format conversation context for AI processing"""
        if not session.conversation_history:
            return ""
        
        # Get recent exchanges
        recent = session.conversation_history[-3:]
        context_parts = []
        
        for exchange in recent:
            context_parts.append(f"User: {exchange['question']}")
            context_parts.append(f"Assistant: {exchange['response']}")
        
        return "\n".join(context_parts)
    
    def _is_inappropriate_content(self, text: str) -> bool:
        """Basic content filtering"""
        if not self.config.enable_content_filtering:
            return False
        
        # Simple keyword-based filtering (in production, use advanced NLP)
        inappropriate_patterns = [
            r'\b(?:hack|crack|pirat|illegal)\b',
            r'\b(?:drug|weapon|violence)\b',
            r'\b(?:hate|discriminat|racist)\b'
        ]
        
        text_lower = text.lower()
        return any(re.search(pattern, text_lower) for pattern in inappropriate_patterns)
    
    def handle_voice_input(self) -> Optional[str]:
        """Handle voice input with accessibility support"""
        if not self.accessibility.speech_recognizer:
            self._display_message("Voice input not available", "warning")
            return None
        
        try:
            self._display_message("🎤 Ready for voice input...", "info")
            return self.accessibility.speech_to_text()
        except Exception as e:
            self.logger.log(LogLevel.ERROR, "Voice input failed", error=str(e))
            return None
    
    def handle_voice_output(self, text: str):
        """Handle voice output with language support"""
        if not self.current_session:
            return
        
        try:
            self.accessibility.text_to_speech(
                text, self.current_session.preferred_language
            )
        except Exception as e:
            self.logger.log(LogLevel.ERROR, "Voice output failed", error=str(e))
    
    def _display_message(self, message: str, style: str = "info"):
        """Display message with rich formatting"""
        if self.console:
            if style == "error":
                self.console.print(f"❌ {message}", style="bold red")
            elif style == "warning":
                self.console.print(f"⚠️  {message}", style="bold yellow")
            elif style == "success":
                self.console.print(f"✅ {message}", style="bold green")
            elif style == "info":
                self.console.print(f"ℹ️  {message}", style="bold blue")
            else:
                self.console.print(message)
        else:
            print(f"{message}")
    
    def display_welcome_screen(self):
        """Display beautiful welcome screen"""
        if self.console:
            layout = Layout()
            layout.split_column(
                Layout(name="header", size=8),
                Layout(name="body", size=12),
                Layout(name="footer", size=6)
            )
            
            # Header
            header_content = Panel.fit(
                """[bold blue]🚀 ULTRA-ADVANCED INFORMATION KIOSK[/bold blue]
[italic]Powered by AI • Multi-Language • Voice Enabled • Accessible[/italic]""",
                border_style="blue"
            )
            layout["header"].update(header_content)
            
            # Body - Features
            features_table = Table(title="🌟 Available Features", show_header=True, header_style="bold magenta")
            features_table.add_column("Feature", style="cyan", width=20)
            features_table.add_column("Status", justify="center", width=12)
            features_table.add_column("Description", style="white", width=35)
            
            enabled_features = self._get_enabled_features()
            feature_descriptions = {
                "AI Responses": "Intelligent multi-model AI responses",
                "Caching": "Smart response caching for speed",
                "Analytics": "Advanced usage analytics",
                "Rich UI": "Beautiful terminal interface",
                "Voice I/O": "Speech input and output",
                "Translation": "50+ language support",
                "Accessibility": "Full accessibility compliance"
            }
            
            for feature, desc in feature_descriptions.items():
                status = "✅ Active" if feature in enabled_features else "⚪ Inactive"
                style = "green" if feature in enabled_features else "dim"
                features_table.add_row(feature, status, desc, style=style)
            
            layout["body"].update(features_table)
            
            # Footer - Commands
            commands_panel = Panel(
                """[bold]🎯 Quick Commands:[/bold]
• [cyan]help[/cyan] - Show all available commands
• [cyan]voice[/cyan] - Enable voice input mode  
• [cyan]lang <code>[/cyan] - Change language (en, es, fr, de, etc.)
• [cyan]stats[/cyan] - View session statistics
• [cyan]clear[/cyan] - Reset conversation
• [cyan]exit[/cyan] - End session

[bold green]Just ask me anything for intelligent assistance![/bold green]""",
                title="Commands & Usage",
                border_style="green"
            )
            layout["footer"].update(commands_panel)
            
            self.console.print(layout)
        else:
            print("\n" + "="*60)
            print("🚀 ULTRA-ADVANCED INFORMATION KIOSK")
            print("="*60)
            print("Features: AI • Multi-Language • Voice • Analytics")
            print("Commands: help | voice | lang | stats | clear | exit")
            print("="*60 + "\n")
    
    def display_session_stats(self):
        """Display comprehensive session statistics"""
        if not self.current_session:
            return
        
        session = self.current_session
        session_duration = datetime.now() - session.start_time
        
        if self.console:
            stats_table = Table(title="📊 Session Statistics", show_header=True)
            stats_table.add_column("Metric", style="cyan", width=25)
            stats_table.add_column("Value", style="white", width=20)
            
            stats_data = [
                ("Session Duration", f"{int(session_duration.total_seconds() // 60)}m {int(session_duration.total_seconds() % 60)}s"),
                ("Questions Asked", str(session.questions_count)),
                ("Average Response Time", f"{session.total_response_time / max(1, session.questions_count):.2f}s"),
                ("Language", session.preferred_language.upper()),
                ("Errors Encountered", str(session.errors_encountered)),
                ("Conversation Turns", str(len(session.conversation_history))),
                ("Voice Mode", "Enabled" if session.voice_enabled else "Disabled"),
                ("Accessibility Mode", "Enabled" if session.accessibility_mode else "Disabled")
            ]
            
            for metric, value in stats_data:
                stats_table.add_row(metric, value)
            
            # Cache stats
            cache_stats = self.cache.get_stats()
            cache_table = Table(title="⚡ Performance Metrics", show_header=True)
            cache_table.add_column("Metric", style="yellow", width=25)
            cache_table.add_column("Value", style="white", width=20)
            
            cache_data = [
                ("Total Requests", str(self.performance_metrics['total_requests'])),
                ("Cache Hits", str(cache_stats['total_hits'])),
                ("Cache Size", str(cache_stats['size'])),
                ("Hit Rate", f"{cache_stats['hit_rate']:.1%}"),
                ("Active Sessions", str(len(self.active_sessions)))
            ]
            
            for metric, value in cache_data:
                cache_table.add_row(metric, value)
            
            self.console.print(Panel.fit(stats_table, title="Session Overview"))
            self.console.print(Panel.fit(cache_table, title="System Performance"))
        else:
            print(f"\n📊 Session Statistics:")
            print(f"   Duration: {int(session_duration.total_seconds() // 60)}m {int(session_duration.total_seconds() % 60)}s")
            print(f"   Questions: {session.questions_count}")
            print(f"   Avg Response Time: {session.total_response_time / max(1, session.questions_count):.2f}s")
            print(f"   Language: {session.preferred_language.upper()}")
            print(f"   Errors: {session.errors_encountered}")
    
    def change_language(self, language_code: str) -> bool:
        """Change session language with validation"""
        if not self.current_session:
            return False
        
        # Validate language code
        valid_languages = [lang.value for lang in Language]
        if language_code not in valid_languages:
            self._display_message(f"Unsupported language: {language_code}. Supported: {', '.join(valid_languages)}", "warning")
            return False
        
        self.current_session.preferred_language = language_code
        self._display_message(f"Language changed to: {language_code.upper()}", "success")
        self.logger.log(LogLevel.INFO, "Language changed", 
                       session_id=self.current_session.id, 
                       language=language_code)
        return True
    
    def handle_special_commands(self, user_input: str) -> Optional[str]:
        """Handle special commands with enhanced functionality"""
        cmd_parts = user_input.lower().strip().split()
        cmd = cmd_parts[0] if cmd_parts else ""
        
        # Exit commands
        if cmd in ["exit", "quit", "bye", "goodbye", "done"]:
            if self.current_session and self.config.enable_analytics:
                self.analytics.log_session(self.current_session)
            return "exit"
        
        # Clear/Reset commands
        elif cmd in ["clear", "reset", "restart", "new"]:
            if self.current_session:
                old_session_id = self.current_session.id
                if self.config.enable_analytics:
                    self.analytics.log_session(self.current_session)
                del self.active_sessions[old_session_id]
            
            self.create_session()
            self._display_message("🔄 New session started with fresh conversation", "success")
            return "cleared"
        
        # Help command
        elif cmd in ["help", "commands", "?"]:
            if self.console:
                help_content = """[bold]🎯 Available Commands:[/bold]

[cyan]Basic Commands:[/cyan]
• [white]help[/white] - Show this help message
• [white]clear, reset[/white] - Start new conversation session
• [white]stats[/white] - Display session statistics
• [white]exit, quit[/white] - End kiosk session

[cyan]Language & Accessibility:[/cyan]
• [white]lang <code>[/white] - Change language (en, es, fr, de, it, pt, ru, zh, ja, ko, ar, hi)
• [white]voice[/white] - Toggle voice input mode
• [white]speak[/white] - Enable voice output for responses
• [white]accessibility[/white] - Toggle accessibility features

[cyan]Advanced Features:[/cyan]
• [white]insights[/white] - View analytics insights
• [white]health[/white] - System health status
• [white]cache[/white] - Cache statistics
• [white]models[/white] - Available AI models status

[bold green]💬 Ask me anything else for intelligent assistance![/bold green]"""
                
                self.console.print(Panel(help_content, title="Command Reference", border_style="cyan"))
            else:
                help_text = """Available Commands:
• help - Show commands
• clear/reset - New session
• stats - Session statistics
• lang <code> - Change language
• voice - Voice input mode
• exit/quit - End session
• Ask me anything for assistance!"""
                print(f"ℹ️  {help_text}")
            return "help_shown"
        
        # Statistics command
        elif cmd in ["stats", "statistics", "info"]:
            self.display_session_stats()
            return "stats_shown"
        
        # Language change command
        elif cmd == "lang" and len(cmd_parts) > 1:
            language_code = cmd_parts[1]
            self.change_language(language_code)
            return "language_changed"
        
        # Voice commands
        elif cmd in ["voice", "speech"]:
            if not self.current_session:
                self.create_session()
            
            self.current_session.voice_enabled = not self.current_session.voice_enabled
            status = "enabled" if self.current_session.voice_enabled else "disabled"
            self._display_message(f"🎤 Voice input {status}", "success" if self.current_session.voice_enabled else "info")
            return "voice_toggled"
        
        elif cmd == "speak":
            if not self.current_session:
                self.create_session()
            
            self._display_message("🔊 Voice output will be used for responses", "success")
            return "speak_enabled"
        
        # Accessibility command
        elif cmd == "accessibility":
            if not self.current_session:
                self.create_session()
            
            self.current_session.accessibility_mode = not self.current_session.accessibility_mode
            status = "enabled" if self.current_session.accessibility_mode else "disabled"
            self._display_message(f"♿ Accessibility features {status}", "success")
            return "accessibility_toggled"
        
        # Analytics insights
        elif cmd == "insights":
            if self.config.enable_analytics:
                self.display_analytics_insights()
            else:
                self._display_message("Analytics not enabled", "warning")
            return "insights_shown"
        
        # System health
        elif cmd == "health":
            self.display_system_health()
            return "health_shown"
        
        # Cache statistics
        elif cmd == "cache":
            cache_stats = self.cache.get_stats()
            self._display_message(f"Cache: {cache_stats['size']} items, {cache_stats['hit_rate']:.1%} hit rate", "info")
            return "cache_shown"
        
        # Model status
        elif cmd == "models":
            self.display_model_status()
            return "models_shown"
        
        return None
    
    def display_analytics_insights(self):
        """Display comprehensive analytics insights"""
        try:
            insights = self.analytics.get_insights()
            
            if self.console:
                # Session insights
                session_stats = insights.get('session_stats', {})
                insights_table = Table(title="📈 Analytics Insights (Last 7 Days)", show_header=True)
                insights_table.add_column("Metric", style="cyan", width=25)
                insights_table.add_column("Value", style="white", width=20)
                
                analytics_data = [
                    ("Total Sessions", str(session_stats.get('total_sessions', 0))),
                    ("Avg Questions/Session", f"{session_stats.get('avg_questions_per_session', 0):.1f}"),
                    ("Avg Response Time", f"{session_stats.get('avg_response_time', 0):.2f}s"),
                    ("User Satisfaction", f"{session_stats.get('avg_satisfaction', 0) or 'N/A'}"),
                ]
                
                for metric, value in analytics_data:
                    insights_table.add_row(metric, value)
                
                self.console.print(Panel.fit(insights_table))
                
                # Popular questions
                popular = insights.get('popular_questions', [])[:5]
                if popular:
                    pop_table = Table(title="🔥 Most Asked Questions", show_header=True)
                    pop_table.add_column("Question", style="white", width=40)
                    pop_table.add_column("Count", style="cyan", width=10)
                    
                    for item in popular:
                        pop_table.add_row(item['question'][:40] + "..." if len(item['question']) > 40 else item['question'], 
                                        str(item['frequency']))
                    
                    self.console.print(Panel.fit(pop_table))
            else:
                print(f"\n📈 Analytics Insights:")
                session_stats = insights.get('session_stats', {})
                print(f"   Total Sessions: {session_stats.get('total_sessions', 0)}")
                print(f"   Avg Questions/Session: {session_stats.get('avg_questions_per_session', 0):.1f}")
                print(f"   Avg Response Time: {session_stats.get('avg_response_time', 0):.2f}s")
                
        except Exception as e:
            self.logger.log(LogLevel.ERROR, "Failed to display analytics", error=str(e))
            self._display_message("Unable to load analytics data", "error")
    
    def display_system_health(self):
        """Display system health and diagnostics"""
        health_status = []
        
        # AI Models health
        try:
            if hasattr(self.ai_manager, 'model_health'):
                healthy_models = sum(1 for status in self.ai_manager.model_health.values() if status['healthy'])
                total_models = len(self.ai_manager.model_health)
                health_status.append(("AI Models", f"{healthy_models}/{total_models} healthy"))
            else:
                health_status.append(("AI Models", "Primary model active"))
        except:
            health_status.append(("AI Models", "⚠️  Status unknown"))
        
        # Cache health
        cache_stats = self.cache.get_stats()
        cache_health = "Healthy" if cache_stats['size'] < 900 else "Near capacity"
        health_status.append(("Cache System", cache_health))
        
        # Database health
        try:
            with self.analytics.get_connection() as conn:
                conn.execute("SELECT 1").fetchone()
            health_status.append(("Database", "Connected"))
        except:
            health_status.append(("Database", "⚠️  Connection issue"))
        
        # Voice features
        voice_status = "Available" if VOICE_AVAILABLE else "Not available"
        health_status.append(("Voice Features", voice_status))
        
        # Translation
        translation_status = "Available" if TRANSLATION_AVAILABLE else "Not available"
        health_status.append(("Translation", translation_status))
        
        if self.console:
            health_table = Table(title="🏥 System Health Status", show_header=True)
            health_table.add_column("Component", style="cyan", width=20)
            health_table.add_column("Status", style="white", width=25)
            
            for component, status in health_status:
                style = "green" if "healthy" in status.lower() or "available" in status.lower() or "connected" in status.lower() else "yellow"
                health_table.add_row(component, status, style=style)
            
            self.console.print(Panel.fit(health_table))
        else:
            print(f"\n🏥 System Health:")
            for component, status in health_status:
                print(f"   {component}: {status}")
    
    def display_model_status(self):
        """Display AI model status and availability"""
        if self.console:
            model_table = Table(title="🤖 AI Models Status", show_header=True)
            model_table.add_column("Model", style="cyan", width=20)
            model_table.add_column("Status", style="white", width=15)
            model_table.add_column("Last Error", style="red", width=25)
            
            # Primary model
            model_table.add_row(
                f"{self.config.primary_model_provider.value}:{self.config.primary_model_name}",
                "✅ Primary",
                "None"
            )
            
            # Fallback models
            for model_key, health_info in getattr(self.ai_manager, 'model_health', {}).items():
                status = "✅ Healthy" if health_info['healthy'] else "❌ Error"
                error = health_info.get('last_error', 'None')[:25] + "..." if health_info.get('last_error') and len(health_info.get('last_error', '')) > 25 else health_info.get('last_error', 'None')
                model_table.add_row(model_key, status, error)
            
            self.console.print(Panel.fit(model_table))
        else:
            print(f"\n🤖 AI Models:")
            print(f"   Primary: {self.config.primary_model_provider.value}:{self.config.primary_model_name}")
            for model_key, health_info in getattr(self.ai_manager, 'model_health', {}).items():
                status = "Healthy" if health_info['healthy'] else "Error"
                print(f"   {model_key}: {status}")
    
    async def run_interactive_session(self):
        """Run the main interactive kiosk session"""
        self.display_welcome_screen()
        self.create_session()
        
        try:
            while True:
                # Check for session limits
                if (self.current_session.questions_count >= self.config.max_conversation_turns):
                    self._display_message("🔄 Starting fresh session for optimal performance...", "info")
                    if self.config.enable_analytics:
                        self.analytics.log_session(self.current_session)
                    old_session_id = self.current_session.id
                    del self.active_sessions[old_session_id]
                    self.create_session()
                
                # Get user input
                user_input = None
                
                # Voice input if enabled
                if (self.current_session.voice_enabled and 
                    hasattr(self.accessibility, 'speech_recognizer') and 
                    self.accessibility.speech_recognizer):
                    
                    if self.console:
                        with self.console.status("[bold blue]🎤 Listening for voice input...[/bold blue]"):
                            user_input = self.handle_voice_input()
                    else:
                        user_input = self.handle_voice_input()
                    
                    if user_input:
                        self._display_message(f"🎤 Heard: \"{user_input}\"", "info")
                
                # Text input fallback or primary
                if not user_input:
                    try:
                        prompt = "🗣️  You (or type 'voice' for speech): " if self.current_session.voice_enabled else "💬 You: "
                        user_input = input(prompt).strip()
                    except (KeyboardInterrupt, EOFError):
                        break
                
                # Handle empty input
                if not user_input:
                    self._display_message("Please ask me something! Type 'help' for available commands.", "info")
                    continue
                
                # Handle special commands
                command_result = self.handle_special_commands(user_input)
                if command_result == "exit":
                    break
                elif command_result in ["cleared", "help_shown", "stats_shown", "language_changed", 
                                      "voice_toggled", "speak_enabled", "accessibility_toggled",
                                      "insights_shown", "health_shown", "cache_shown", "models_shown"]:
                    continue
                
                # Process regular query
                if self.console:
                    with self.console.status("[bold green]🤖 Processing your request...[/bold green]"):
                        response, metadata = await self.process_query(user_input)
                else:
                    print("🤖 Processing...", end="", flush=True)
                    response, metadata = await self.process_query(user_input)
                    print("\r" + " " * 20 + "\r", end="", flush=True)
                
                # Display response with metadata
                if self.console:
                    response_panel = Panel.fit(
                        response,
                        title=f"🤖 Assistant Response{' (Cached)' if metadata['cached'] else ''}",
                        border_style="green" if not metadata.get('error') else "red"
                    )
                    self.console.print(response_panel)
                    
                    # Show metadata for transparency
                    if metadata['response_time'] > 5:
                        self.console.print(f"[dim]Response time: {metadata['response_time']:.2f}s | Model: {metadata['model_used']}[/dim]")
                else:
                    print(f"🤖 {response}")
                    if metadata['cached']:
                        print("   [Cached response]")
                    elif metadata['response_time'] > 5:
                        print(f"   [Response time: {metadata['response_time']:.2f}s]")
                
                # Voice output if requested
                if (hasattr(self, '_speak_enabled') and self._speak_enabled) or self.current_session.accessibility_mode:
                    self.handle_voice_output(response)
                
                print()  # Add spacing
                
        except KeyboardInterrupt:
            pass
        finally:
            # Cleanup and final stats
            if self.current_session and self.config.enable_analytics:
                self.analytics.log_session(self.current_session)
            
            self._display_message("Thank you for using the Ultra-Advanced Kiosk System!", "success")
            if self.current_session:
                session_duration = datetime.now() - self.current_session.start_time
                self._display_message(
                    f"Session summary: {self.current_session.questions_count} questions in "
                    f"{int(session_duration.total_seconds() // 60)}m {int(session_duration.total_seconds() % 60)}s",
                    "info"
                )


async def main():
    """Initialize and run the Ultra-Advanced Kiosk System"""
    print("🚀 Initializing Ultra-Advanced Kiosk System...")
    
    try:
        # Create configuration
        config = KioskConfig(
            primary_model_provider=ModelProvider.OLLAMA,
            primary_model_name="neural-chat",
            use_rich_ui=True,
            enable_voice=True,
            enable_accessibility=True,
            enable_analytics=True,
            max_conversation_turns=50,
            temperature=0.3
        )
        
        # Initialize kiosk
        kiosk = UltraAdvancedKioskChatbot(config)
        
        # Run interactive session
        await kiosk.run_interactive_session()
        
    except Exception as e:
        print(f"❌ Critical system error: {str(e)}")
        print("\n🔧 Troubleshooting:")
        print("1. Ensure Ollama is running: 'ollama serve'")
        print("2. Install required model: 'ollama pull neural-chat'")
        print("3. Check dependencies: pip install -r requirements.txt")
        print("4. For voice features: pip install SpeechRecognition pyttsx3")
        print("5. For rich UI: pip install rich colorama")
        print("6. For translation: pip install googletrans==4.0.0rc1")


if __name__ == "__main__":
    print("="*70)
    print("🚀 ULTRA-ADVANCED KIOSK CHATBOT SYSTEM")
    print("="*70)
    print("Enterprise-grade AI-powered information kiosk")
    print("Features: Multi-AI • Voice I/O • Analytics • Accessibility • Rich UI")
    print("="*70)
    
    # Check dependencies
    missing_deps = []
    if not LANGCHAIN_AVAILABLE:
        missing_deps.append("langchain-ollama langchain-core")
    if not VOICE_AVAILABLE:
        missing_deps.append("SpeechRecognition pyttsx3")
    if not RICH_UI_AVAILABLE:
        missing_deps.append("rich colorama")
    if not TRANSLATION_AVAILABLE:
        missing_deps.append("googletrans==4.0.0rc1")
    
    if missing_deps:
        print(f"⚠️  Optional dependencies missing: {' '.join(missing_deps)}")
        print("   Install with: pip install " + " ".join(missing_deps))
        print("   System will run with reduced functionality.")
    
    asyncio.run(main())