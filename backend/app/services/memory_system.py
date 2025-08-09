"""
DataSoph AI - Advanced Memory and Session Management System
Intelligent conversation continuity with context awareness and learning
"""

import json
import sqlite3
import pickle
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from pathlib import Path
import logging
import hashlib
import uuid
from enum import Enum

logger = logging.getLogger(__name__)

class MemoryType(Enum):
    """Types of memories in the system"""
    CONVERSATION = "conversation"
    USER_PREFERENCE = "user_preference"
    ANALYSIS_RESULT = "analysis_result"
    BUSINESS_INSIGHT = "business_insight"
    MODEL_PERFORMANCE = "model_performance"
    DATA_PATTERN = "data_pattern"
    DOMAIN_KNOWLEDGE = "domain_knowledge"

class ContextImportance(Enum):
    """Importance levels for context retention"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

@dataclass
class Memory:
    """Individual memory item with metadata"""
    memory_id: str
    user_id: str
    memory_type: MemoryType
    content: Dict[str, Any]
    importance: ContextImportance
    created_at: datetime
    last_accessed: datetime
    access_count: int
    context_tags: List[str]
    associated_files: List[str]
    confidence_score: float
    expires_at: Optional[datetime] = None

@dataclass
class ConversationSession:
    """Complete conversation session with all context"""
    session_id: str
    user_id: str
    start_time: datetime
    last_activity: datetime
    total_interactions: int
    conversation_thread: List[Dict[str, Any]]
    uploaded_files: List[str]
    analysis_results: List[str]
    user_expertise_level: str
    primary_language: str
    conversation_mood: str
    session_goals: List[str]
    achieved_objectives: List[str]

class ConversationMemory:
    """
    Advanced conversation memory system with intelligent context management
    """
    
    def __init__(self, db_path: str = "datasoph_memory.db"):
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)
        
        # Memory retention policies
        self.retention_policies = {
            MemoryType.CONVERSATION: timedelta(days=30),
            MemoryType.USER_PREFERENCE: timedelta(days=365),
            MemoryType.ANALYSIS_RESULT: timedelta(days=90),
            MemoryType.BUSINESS_INSIGHT: timedelta(days=180),
            MemoryType.MODEL_PERFORMANCE: timedelta(days=60),
            MemoryType.DATA_PATTERN: timedelta(days=120),
            MemoryType.DOMAIN_KNOWLEDGE: timedelta(days=730)  # 2 years
        }
        
        # Context similarity thresholds
        self.similarity_thresholds = {
            'high': 0.8,
            'medium': 0.6,
            'low': 0.4
        }
        
        # Initialize database
        self._initialize_database()
        
        # In-memory caches for performance
        self.session_cache: Dict[str, ConversationSession] = {}
        self.user_preference_cache: Dict[str, Dict[str, Any]] = {}
        self.recent_memories_cache: Dict[str, List[Memory]] = {}
        
        self.logger.info("🧠 Advanced Memory System initialized")

    def _initialize_database(self):
        """Initialize SQLite database for persistent memory storage"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Memories table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS memories (
                    memory_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    memory_type TEXT NOT NULL,
                    content TEXT NOT NULL,
                    importance TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    last_accessed TEXT NOT NULL,
                    access_count INTEGER DEFAULT 0,
                    context_tags TEXT NOT NULL,
                    associated_files TEXT NOT NULL,
                    confidence_score REAL NOT NULL,
                    expires_at TEXT
                )
            ''')
            
            # Conversation sessions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS conversation_sessions (
                    session_id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    start_time TEXT NOT NULL,
                    last_activity TEXT NOT NULL,
                    total_interactions INTEGER DEFAULT 0,
                    conversation_thread TEXT NOT NULL,
                    uploaded_files TEXT NOT NULL,
                    analysis_results TEXT NOT NULL,
                    user_expertise_level TEXT,
                    primary_language TEXT,
                    conversation_mood TEXT,
                    session_goals TEXT NOT NULL,
                    achieved_objectives TEXT NOT NULL
                )
            ''')
            
            # User profiles table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS user_profiles (
                    user_id TEXT PRIMARY KEY,
                    profile_data TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    last_updated TEXT NOT NULL
                )
            ''')
            
            # Create indexes for performance
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_memories_user_id ON memories(user_id)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_memories_type ON memories(memory_type)')
            cursor.execute('CREATE INDEX IF NOT EXISTS idx_sessions_user_id ON conversation_sessions(user_id)')
            
            conn.commit()
            conn.close()
            
            self.logger.info("✅ Memory database initialized successfully")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize memory database: {e}")
            raise

    def create_memory(self, user_id: str, memory_type: MemoryType, content: Dict[str, Any],
                     importance: ContextImportance = ContextImportance.MEDIUM,
                     context_tags: List[str] = None, associated_files: List[str] = None,
                     confidence_score: float = 1.0) -> str:
        """Create a new memory with intelligent categorization"""
        
        try:
            memory_id = str(uuid.uuid4())
            now = datetime.now()
            
            # Auto-generate context tags if not provided
            if context_tags is None:
                context_tags = self._generate_context_tags(content, memory_type)
            
            if associated_files is None:
                associated_files = []
            
            # Calculate expiration based on retention policy
            expires_at = None
            if memory_type in self.retention_policies:
                expires_at = now + self.retention_policies[memory_type]
            
            memory = Memory(
                memory_id=memory_id,
                user_id=user_id,
                memory_type=memory_type,
                content=content,
                importance=importance,
                created_at=now,
                last_accessed=now,
                access_count=1,
                context_tags=context_tags,
                associated_files=associated_files,
                confidence_score=confidence_score,
                expires_at=expires_at
            )
            
            # Store in database
            self._store_memory(memory)
            
            # Update cache
            self._update_memory_cache(user_id, memory)
            
            self.logger.info(f"💾 Created memory {memory_id} for user {user_id}")
            return memory_id
            
        except Exception as e:
            self.logger.error(f"❌ Failed to create memory: {e}")
            raise

    def retrieve_relevant_memories(self, user_id: str, context: Dict[str, Any], 
                                 limit: int = 10) -> List[Memory]:
        """Retrieve memories relevant to current context using intelligent matching"""
        
        try:
            # Generate context tags for current context
            current_tags = self._generate_context_tags(context, MemoryType.CONVERSATION)
            
            # Get all user memories
            user_memories = self._get_user_memories(user_id)
            
            # Score memories by relevance
            scored_memories = []
            for memory in user_memories:
                relevance_score = self._calculate_relevance_score(memory, current_tags, context)
                if relevance_score > self.similarity_thresholds['low']:
                    scored_memories.append((memory, relevance_score))
            
            # Sort by relevance and recency
            scored_memories.sort(key=lambda x: (x[1], x[0].last_accessed), reverse=True)
            
            # Update access patterns
            relevant_memories = [mem for mem, score in scored_memories[:limit]]
            for memory in relevant_memories:
                self._update_memory_access(memory.memory_id)
            
            self.logger.info(f"🎯 Retrieved {len(relevant_memories)} relevant memories for user {user_id}")
            return relevant_memories
            
        except Exception as e:
            self.logger.error(f"❌ Failed to retrieve relevant memories: {e}")
            return []

    def maintain_context(self, user_id: str, new_interaction: Dict[str, Any], 
                        session_id: str = None) -> ConversationSession:
        """Maintain conversation context with intelligent context preservation"""
        
        try:
            # Get or create session
            if session_id and session_id in self.session_cache:
                session = self.session_cache[session_id]
            else:
                session = self._get_or_create_session(user_id, session_id)
            
            # Update session with new interaction
            session.last_activity = datetime.now()
            session.total_interactions += 1
            session.conversation_thread.append({
                'timestamp': datetime.now().isoformat(),
                'interaction': new_interaction,
                'context_snapshot': self._create_context_snapshot(user_id)
            })
            
            # Analyze interaction for insights
            insights = self._analyze_interaction_for_insights(new_interaction, session)
            if insights:
                for insight in insights:
                    self.create_memory(
                        user_id=user_id,
                        memory_type=MemoryType.CONVERSATION,
                        content=insight,
                        importance=ContextImportance.MEDIUM,
                        context_tags=insight.get('tags', [])
                    )
            
            # Update user preferences based on interaction
            self._update_user_preferences(user_id, new_interaction, session)
            
            # Manage session length (keep last N interactions in active memory)
            if len(session.conversation_thread) > 50:  # Configurable limit
                # Archive older interactions to persistent memory
                self._archive_old_interactions(session)
            
            # Update session in cache and database
            self.session_cache[session.session_id] = session
            self._store_session(session)
            
            self.logger.info(f"🔄 Updated context for user {user_id}, session {session.session_id}")
            return session
            
        except Exception as e:
            self.logger.error(f"❌ Failed to maintain context: {e}")
            return self._create_new_session(user_id)

    def get_conversation_history(self, user_id: str, session_id: str = None, 
                               limit: int = 20) -> List[Dict[str, Any]]:
        """Get conversation history with intelligent summarization"""
        
        try:
            if session_id:
                # Get specific session history
                session = self._get_session(session_id)
                if session and session.user_id == user_id:
                    return session.conversation_thread[-limit:]
            
            # Get recent conversations across all sessions
            user_memories = self._get_user_memories(user_id, MemoryType.CONVERSATION)
            recent_conversations = []
            
            for memory in sorted(user_memories, key=lambda x: x.last_accessed, reverse=True)[:limit]:
                if 'interaction' in memory.content:
                    recent_conversations.append({
                        'timestamp': memory.created_at.isoformat(),
                        'content': memory.content,
                        'context_tags': memory.context_tags,
                        'memory_id': memory.memory_id
                    })
            
            return recent_conversations
            
        except Exception as e:
            self.logger.error(f"❌ Failed to get conversation history: {e}")
            return []

    def update_user_expertise(self, user_id: str, expertise_indicators: Dict[str, Any]):
        """Update user expertise level based on interaction patterns"""
        
        try:
            # Get current user profile
            profile = self._get_user_profile(user_id)
            
            # Analyze expertise indicators
            current_level = profile.get('expertise_level', 'intermediate')
            
            # Technical language usage
            technical_score = expertise_indicators.get('technical_language_score', 0.5)
            
            # Complexity of questions asked
            question_complexity = expertise_indicators.get('question_complexity', 0.5)
            
            # Understanding of responses
            response_comprehension = expertise_indicators.get('response_comprehension', 0.5)
            
            # Calculate new expertise level
            expertise_score = (technical_score + question_complexity + response_comprehension) / 3
            
            if expertise_score > 0.8:
                new_level = 'expert'
            elif expertise_score > 0.6:
                new_level = 'advanced'
            elif expertise_score > 0.4:
                new_level = 'intermediate'
            else:
                new_level = 'beginner'
            
            # Update profile if level changed
            if new_level != current_level:
                profile['expertise_level'] = new_level
                profile['expertise_updated_at'] = datetime.now().isoformat()
                
                # Create memory for expertise change
                self.create_memory(
                    user_id=user_id,
                    memory_type=MemoryType.USER_PREFERENCE,
                    content={
                        'type': 'expertise_level_change',
                        'old_level': current_level,
                        'new_level': new_level,
                        'score': expertise_score
                    },
                    importance=ContextImportance.HIGH
                )
                
                self._store_user_profile(user_id, profile)
                self.logger.info(f"📈 Updated expertise level for user {user_id}: {current_level} → {new_level}")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to update user expertise: {e}")

    def get_conversation_summary(self, user_id: str, session_id: str = None, 
                               time_period: timedelta = None) -> Dict[str, Any]:
        """Generate intelligent conversation summary"""
        
        try:
            if time_period is None:
                time_period = timedelta(days=7)  # Last week by default
            
            cutoff_time = datetime.now() - time_period
            
            # Get relevant memories
            if session_id:
                session = self._get_session(session_id)
                interactions = session.conversation_thread if session else []
            else:
                memories = self._get_user_memories(user_id, MemoryType.CONVERSATION)
                interactions = [m.content for m in memories if m.created_at >= cutoff_time]
            
            if not interactions:
                return {'summary': 'No recent conversation activity'}
            
            # Analyze interaction patterns
            summary = {
                'total_interactions': len(interactions),
                'time_period': str(time_period),
                'primary_topics': self._extract_main_topics(interactions),
                'files_analyzed': self._count_files_analyzed(interactions),
                'expertise_progression': self._assess_expertise_progression(user_id, cutoff_time),
                'preferred_analysis_types': self._identify_preferred_analysis_types(interactions),
                'language_preference': self._determine_language_preference(interactions),
                'session_goals_achieved': self._assess_goal_achievement(user_id, session_id),
                'recommendations': self._generate_summary_recommendations(interactions, user_id)
            }
            
            return summary
            
        except Exception as e:
            self.logger.error(f"❌ Failed to generate conversation summary: {e}")
            return {'error': str(e)}

    def cleanup_expired_memories(self):
        """Clean up expired memories and optimize storage"""
        
        try:
            now = datetime.now()
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Delete expired memories
            cursor.execute('''
                DELETE FROM memories 
                WHERE expires_at IS NOT NULL AND expires_at < ?
            ''', (now.isoformat(),))
            
            deleted_count = cursor.rowcount
            
            # Clean up old sessions (older than 30 days with no activity)
            session_cutoff = now - timedelta(days=30)
            cursor.execute('''
                DELETE FROM conversation_sessions 
                WHERE last_activity < ?
            ''', (session_cutoff.isoformat(),))
            
            sessions_deleted = cursor.rowcount
            
            conn.commit()
            conn.close()
            
            # Clear relevant caches
            self._clear_expired_caches()
            
            self.logger.info(f"🧹 Cleanup completed: {deleted_count} memories, {sessions_deleted} sessions removed")
            
        except Exception as e:
            self.logger.error(f"❌ Memory cleanup failed: {e}")

    def export_user_memory(self, user_id: str) -> Dict[str, Any]:
        """Export user's complete memory for backup or transfer"""
        
        try:
            user_memories = self._get_user_memories(user_id)
            user_sessions = self._get_user_sessions(user_id)
            user_profile = self._get_user_profile(user_id)
            
            export_data = {
                'user_id': user_id,
                'export_timestamp': datetime.now().isoformat(),
                'memories': [asdict(memory) for memory in user_memories],
                'sessions': [asdict(session) for session in user_sessions],
                'profile': user_profile,
                'total_memories': len(user_memories),
                'total_sessions': len(user_sessions)
            }
            
            self.logger.info(f"📤 Exported memory for user {user_id}: {len(user_memories)} memories, {len(user_sessions)} sessions")
            return export_data
            
        except Exception as e:
            self.logger.error(f"❌ Failed to export user memory: {e}")
            return {'error': str(e)}

    # Helper methods for memory management

    def _generate_context_tags(self, content: Dict[str, Any], memory_type: MemoryType) -> List[str]:
        """Generate context tags for content"""
        tags = []
        
        # Add memory type tag
        tags.append(f"type:{memory_type.value}")
        
        # Extract content-based tags
        if isinstance(content, dict):
            for key, value in content.items():
                if key in ['intent', 'language', 'file_type', 'analysis_type']:
                    tags.append(f"{key}:{value}")
                elif key == 'message' and isinstance(value, str):
                    # Extract keywords from message
                    keywords = self._extract_keywords(value)
                    tags.extend([f"keyword:{kw}" for kw in keywords[:5]])
        
        return tags

    def _extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text"""
        # Simple keyword extraction
        data_science_keywords = [
            'analysis', 'data', 'chart', 'graph', 'model', 'prediction', 'correlation',
            'statistics', 'visualization', 'machine learning', 'regression', 'classification'
        ]
        
        text_lower = text.lower()
        found_keywords = [kw for kw in data_science_keywords if kw in text_lower]
        return found_keywords

    def _calculate_relevance_score(self, memory: Memory, current_tags: List[str], 
                                 context: Dict[str, Any]) -> float:
        """Calculate relevance score between memory and current context"""
        
        # Tag similarity
        memory_tags = set(memory.context_tags)
        current_tag_set = set(current_tags)
        tag_overlap = len(memory_tags & current_tag_set)
        tag_similarity = tag_overlap / max(len(memory_tags | current_tag_set), 1)
        
        # Recency factor
        days_since_access = (datetime.now() - memory.last_accessed).days
        recency_factor = max(0, 1 - (days_since_access / 30))  # Decay over 30 days
        
        # Importance factor
        importance_weights = {
            ContextImportance.CRITICAL: 1.0,
            ContextImportance.HIGH: 0.8,
            ContextImportance.MEDIUM: 0.6,
            ContextImportance.LOW: 0.4
        }
        importance_factor = importance_weights[memory.importance]
        
        # Access frequency factor
        access_factor = min(memory.access_count / 10, 1.0)  # Cap at 10 accesses
        
        # Combined score
        relevance_score = (
            tag_similarity * 0.4 +
            recency_factor * 0.3 +
            importance_factor * 0.2 +
            access_factor * 0.1
        ) * memory.confidence_score
        
        return relevance_score

    def _store_memory(self, memory: Memory):
        """Store memory in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO memories 
            (memory_id, user_id, memory_type, content, importance, created_at, 
             last_accessed, access_count, context_tags, associated_files, 
             confidence_score, expires_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            memory.memory_id,
            memory.user_id,
            memory.memory_type.value,
            json.dumps(memory.content),
            memory.importance.value,
            memory.created_at.isoformat(),
            memory.last_accessed.isoformat(),
            memory.access_count,
            json.dumps(memory.context_tags),
            json.dumps(memory.associated_files),
            memory.confidence_score,
            memory.expires_at.isoformat() if memory.expires_at else None
        ))
        
        conn.commit()
        conn.close()

    def _get_user_memories(self, user_id: str, memory_type: MemoryType = None) -> List[Memory]:
        """Get all memories for a user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if memory_type:
            cursor.execute('''
                SELECT * FROM memories 
                WHERE user_id = ? AND memory_type = ?
                ORDER BY last_accessed DESC
            ''', (user_id, memory_type.value))
        else:
            cursor.execute('''
                SELECT * FROM memories 
                WHERE user_id = ?
                ORDER BY last_accessed DESC
            ''', (user_id,))
        
        rows = cursor.fetchall()
        conn.close()
        
        memories = []
        for row in rows:
            memory = Memory(
                memory_id=row[0],
                user_id=row[1],
                memory_type=MemoryType(row[2]),
                content=json.loads(row[3]),
                importance=ContextImportance(row[4]),
                created_at=datetime.fromisoformat(row[5]),
                last_accessed=datetime.fromisoformat(row[6]),
                access_count=row[7],
                context_tags=json.loads(row[8]),
                associated_files=json.loads(row[9]),
                confidence_score=row[10],
                expires_at=datetime.fromisoformat(row[11]) if row[11] else None
            )
            memories.append(memory)
        
        return memories

    def _update_memory_access(self, memory_id: str):
        """Update memory access timestamp and count"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE memories 
            SET last_accessed = ?, access_count = access_count + 1
            WHERE memory_id = ?
        ''', (datetime.now().isoformat(), memory_id))
        
        conn.commit()
        conn.close()

    def _get_or_create_session(self, user_id: str, session_id: str = None) -> ConversationSession:
        """Get existing session or create new one"""
        if session_id:
            session = self._get_session(session_id)
            if session and session.user_id == user_id:
                return session
        
        return self._create_new_session(user_id)

    def _create_new_session(self, user_id: str) -> ConversationSession:
        """Create new conversation session"""
        session_id = str(uuid.uuid4())
        now = datetime.now()
        
        session = ConversationSession(
            session_id=session_id,
            user_id=user_id,
            start_time=now,
            last_activity=now,
            total_interactions=0,
            conversation_thread=[],
            uploaded_files=[],
            analysis_results=[],
            user_expertise_level='intermediate',
            primary_language='Turkish',
            conversation_mood='professional',
            session_goals=[],
            achieved_objectives=[]
        )
        
        return session

    def _store_session(self, session: ConversationSession):
        """Store session in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO conversation_sessions
            (session_id, user_id, start_time, last_activity, total_interactions,
             conversation_thread, uploaded_files, analysis_results, user_expertise_level,
             primary_language, conversation_mood, session_goals, achieved_objectives)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            session.session_id,
            session.user_id,
            session.start_time.isoformat(),
            session.last_activity.isoformat(),
            session.total_interactions,
            json.dumps(session.conversation_thread),
            json.dumps(session.uploaded_files),
            json.dumps(session.analysis_results),
            session.user_expertise_level,
            session.primary_language,
            session.conversation_mood,
            json.dumps(session.session_goals),
            json.dumps(session.achieved_objectives)
        ))
        
        conn.commit()
        conn.close()

    def _get_session(self, session_id: str) -> Optional[ConversationSession]:
        """Get session from database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM conversation_sessions WHERE session_id = ?', (session_id,))
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
        
        session = ConversationSession(
            session_id=row[0],
            user_id=row[1],
            start_time=datetime.fromisoformat(row[2]),
            last_activity=datetime.fromisoformat(row[3]),
            total_interactions=row[4],
            conversation_thread=json.loads(row[5]),
            uploaded_files=json.loads(row[6]),
            analysis_results=json.loads(row[7]),
            user_expertise_level=row[8],
            primary_language=row[9],
            conversation_mood=row[10],
            session_goals=json.loads(row[11]),
            achieved_objectives=json.loads(row[12])
        )
        
        return session

    # Additional helper methods would continue here...
    def _update_memory_cache(self, user_id: str, memory: Memory):
        """Update in-memory cache"""
        if user_id not in self.recent_memories_cache:
            self.recent_memories_cache[user_id] = []
        
        self.recent_memories_cache[user_id].insert(0, memory)
        # Keep only recent 50 memories in cache
        self.recent_memories_cache[user_id] = self.recent_memories_cache[user_id][:50]

    def _create_context_snapshot(self, user_id: str) -> Dict[str, Any]:
        """Create snapshot of current context"""
        return {
            'timestamp': datetime.now().isoformat(),
            'active_files': len(self.session_cache.get(user_id, ConversationSession('', '', datetime.now(), datetime.now(), 0, [], [], [], '', '', '', [], [])).uploaded_files),
            'recent_analysis_count': len(self.recent_memories_cache.get(user_id, [])),
            'session_active': user_id in self.session_cache
        }

    def _analyze_interaction_for_insights(self, interaction: Dict[str, Any], 
                                        session: ConversationSession) -> List[Dict[str, Any]]:
        """Analyze interaction for extractable insights"""
        insights = []
        
        # Check for file uploads
        if 'file_id' in interaction:
            insights.append({
                'type': 'file_uploaded',
                'file_id': interaction['file_id'],
                'tags': ['file_upload', 'data_input']
            })
        
        # Check for analysis requests
        if 'message' in interaction:
            message = interaction['message'].lower()
            if any(word in message for word in ['analyze', 'analysis', 'chart', 'graph', 'model']):
                insights.append({
                    'type': 'analysis_request',
                    'request_type': 'data_analysis',
                    'tags': ['analysis', 'data_science']
                })
        
        return insights

    def _update_user_preferences(self, user_id: str, interaction: Dict[str, Any], 
                               session: ConversationSession):
        """Update user preferences based on interaction"""
        # This would analyze interaction patterns and update preferences
        pass

    def _archive_old_interactions(self, session: ConversationSession):
        """Archive old interactions to free up active memory"""
        # Keep last 30 interactions in active memory
        if len(session.conversation_thread) > 30:
            archived_interactions = session.conversation_thread[:-30]
            session.conversation_thread = session.conversation_thread[-30:]
            
            # Store archived interactions as memories
            for interaction in archived_interactions:
                self.create_memory(
                    user_id=session.user_id,
                    memory_type=MemoryType.CONVERSATION,
                    content=interaction,
                    importance=ContextImportance.LOW
                )

    def _get_user_profile(self, user_id: str) -> Dict[str, Any]:
        """Get user profile from database"""
        if user_id in self.user_preference_cache:
            return self.user_preference_cache[user_id]
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT profile_data FROM user_profiles WHERE user_id = ?', (user_id,))
        row = cursor.fetchone()
        conn.close()
        
        if row:
            profile = json.loads(row[0])
        else:
            profile = {
                'expertise_level': 'intermediate',
                'preferred_language': 'Turkish',
                'conversation_style': 'professional',
                'created_at': datetime.now().isoformat()
            }
        
        self.user_preference_cache[user_id] = profile
        return profile

    def _store_user_profile(self, user_id: str, profile: Dict[str, Any]):
        """Store user profile in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT OR REPLACE INTO user_profiles (user_id, profile_data, created_at, last_updated)
            VALUES (?, ?, ?, ?)
        ''', (
            user_id,
            json.dumps(profile),
            profile.get('created_at', datetime.now().isoformat()),
            datetime.now().isoformat()
        ))
        
        conn.commit()
        conn.close()
        
        self.user_preference_cache[user_id] = profile

    def _clear_expired_caches(self):
        """Clear expired cache entries"""
        # Clear old cache entries
        cutoff_time = datetime.now() - timedelta(hours=24)
        
        # This would implement cache cleanup logic
        pass

    def _get_user_sessions(self, user_id: str) -> List[ConversationSession]:
        """Get all sessions for a user"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM conversation_sessions WHERE user_id = ?', (user_id,))
        rows = cursor.fetchall()
        conn.close()
        
        sessions = []
        for row in rows:
            session = ConversationSession(
                session_id=row[0],
                user_id=row[1],
                start_time=datetime.fromisoformat(row[2]),
                last_activity=datetime.fromisoformat(row[3]),
                total_interactions=row[4],
                conversation_thread=json.loads(row[5]),
                uploaded_files=json.loads(row[6]),
                analysis_results=json.loads(row[7]),
                user_expertise_level=row[8],
                primary_language=row[9],
                conversation_mood=row[10],
                session_goals=json.loads(row[11]),
                achieved_objectives=json.loads(row[12])
            )
            sessions.append(session)
        
        return sessions

    # Summary generation methods
    def _extract_main_topics(self, interactions: List[Dict[str, Any]]) -> List[str]:
        """Extract main topics from interactions"""
        topics = set()
        for interaction in interactions:
            if 'context_tags' in interaction:
                topics.update([tag for tag in interaction['context_tags'] if tag.startswith('keyword:')])
        return list(topics)[:10]

    def _count_files_analyzed(self, interactions: List[Dict[str, Any]]) -> int:
        """Count files analyzed in interactions"""
        files = set()
        for interaction in interactions:
            if 'file_id' in interaction.get('interaction', {}):
                files.add(interaction['interaction']['file_id'])
        return len(files)

    def _assess_expertise_progression(self, user_id: str, cutoff_time: datetime) -> str:
        """Assess user expertise progression"""
        profile = self._get_user_profile(user_id)
        return f"Current level: {profile.get('expertise_level', 'unknown')}"

    def _identify_preferred_analysis_types(self, interactions: List[Dict[str, Any]]) -> List[str]:
        """Identify preferred analysis types"""
        analysis_types = ['data_analysis', 'visualization', 'machine_learning', 'statistics']
        return analysis_types[:3]  # Simplified

    def _determine_language_preference(self, interactions: List[Dict[str, Any]]) -> str:
        """Determine language preference from interactions"""
        return 'Turkish'  # Simplified

    def _assess_goal_achievement(self, user_id: str, session_id: str = None) -> Dict[str, Any]:
        """Assess goal achievement"""
        return {'goals_set': 0, 'goals_achieved': 0, 'success_rate': 0}

    def _generate_summary_recommendations(self, interactions: List[Dict[str, Any]], 
                                        user_id: str) -> List[str]:
        """Generate recommendations based on interaction summary"""
        return [
            "Continue regular data analysis practice",
            "Explore advanced visualization techniques",
            "Consider machine learning applications"
        ] 