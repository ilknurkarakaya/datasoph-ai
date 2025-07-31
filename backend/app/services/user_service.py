"""
DATASOPH AI - User Service
Business logic for user management and operations
"""

from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import Optional, List
from datetime import datetime
import logging

from app.models.user import User
from app.core.database import get_db

logger = logging.getLogger(__name__)

class UserService:
    """Service class for user management operations"""
    
    def __init__(self, db: Session):
        self.db = db
    
    async def create_or_get_user(
        self,
        firebase_uid: str,
        email: str,
        name: Optional[str] = None,
        picture: Optional[str] = None
    ) -> User:
        """
        Create a new user or get existing user by Firebase UID
        """
        try:
            # Check if user already exists
            existing_user = self.db.query(User).filter(
                User.firebase_uid == firebase_uid
            ).first()
            
            if existing_user:
                # Update user information if provided
                if name and existing_user.name != name:
                    existing_user.name = name
                if picture and existing_user.picture != picture:
                    existing_user.picture = picture
                if email and existing_user.email != email:
                    existing_user.email = email
                
                existing_user.updated_at = datetime.utcnow()
                self.db.commit()
                self.db.refresh(existing_user)
                
                logger.info(f"Updated existing user: {existing_user.email}")
                return existing_user
            
            # Create new user
            new_user = User(
                firebase_uid=firebase_uid,
                email=email,
                name=name,
                picture=picture,
                is_active=True,
                is_verified=True  # Firebase users are considered verified
            )
            
            self.db.add(new_user)
            self.db.commit()
            self.db.refresh(new_user)
            
            logger.info(f"Created new user: {new_user.email}")
            return new_user
            
        except Exception as e:
            logger.error(f"Error creating/getting user: {e}")
            self.db.rollback()
            raise
    
    async def get_user_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID"""
        try:
            user = self.db.query(User).filter(User.id == user_id).first()
            return user
        except Exception as e:
            logger.error(f"Error getting user by ID {user_id}: {e}")
            return None
    
    async def get_user_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        try:
            user = self.db.query(User).filter(User.email == email).first()
            return user
        except Exception as e:
            logger.error(f"Error getting user by email {email}: {e}")
            return None
    
    async def get_user_by_firebase_uid(self, firebase_uid: str) -> Optional[User]:
        """Get user by Firebase UID"""
        try:
            user = self.db.query(User).filter(User.firebase_uid == firebase_uid).first()
            return user
        except Exception as e:
            logger.error(f"Error getting user by Firebase UID {firebase_uid}: {e}")
            return None
    
    async def update_user_profile(
        self,
        user_id: int,
        name: Optional[str] = None,
        picture: Optional[str] = None,
        preferred_model: Optional[str] = None,
        theme: Optional[str] = None,
        language: Optional[str] = None
    ) -> Optional[User]:
        """Update user profile information"""
        try:
            user = await self.get_user_by_id(user_id)
            if not user:
                return None
            
            # Update fields if provided
            if name is not None:
                user.name = name
            if picture is not None:
                user.picture = picture
            if preferred_model is not None:
                user.preferred_model = preferred_model
            if theme is not None:
                user.theme = theme
            if language is not None:
                user.language = language
            
            user.updated_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(user)
            
            logger.info(f"Updated user profile: {user.email}")
            return user
            
        except Exception as e:
            logger.error(f"Error updating user profile {user_id}: {e}")
            self.db.rollback()
            return None
    
    async def update_last_login(self, user_id: int) -> bool:
        """Update user's last login timestamp"""
        try:
            user = await self.get_user_by_id(user_id)
            if not user:
                return False
            
            user.last_login = datetime.utcnow()
            self.db.commit()
            
            return True
            
        except Exception as e:
            logger.error(f"Error updating last login for user {user_id}: {e}")
            self.db.rollback()
            return False
    
    async def deactivate_user(self, user_id: int) -> bool:
        """Deactivate user account"""
        try:
            user = await self.get_user_by_id(user_id)
            if not user:
                return False
            
            user.is_active = False
            user.updated_at = datetime.utcnow()
            self.db.commit()
            
            logger.info(f"Deactivated user: {user.email}")
            return True
            
        except Exception as e:
            logger.error(f"Error deactivating user {user_id}: {e}")
            self.db.rollback()
            return False
    
    async def activate_user(self, user_id: int) -> bool:
        """Activate user account"""
        try:
            user = await self.get_user_by_id(user_id)
            if not user:
                return False
            
            user.is_active = True
            user.updated_at = datetime.utcnow()
            self.db.commit()
            
            logger.info(f"Activated user: {user.email}")
            return True
            
        except Exception as e:
            logger.error(f"Error activating user {user_id}: {e}")
            self.db.rollback()
            return False
    
    async def get_users_list(
        self,
        skip: int = 0,
        limit: int = 100,
        active_only: bool = True
    ) -> List[User]:
        """Get list of users with pagination"""
        try:
            query = self.db.query(User)
            
            if active_only:
                query = query.filter(User.is_active == True)
            
            users = query.offset(skip).limit(limit).all()
            return users
            
        except Exception as e:
            logger.error(f"Error getting users list: {e}")
            return []
    
    async def get_user_stats(self, user_id: int) -> dict:
        """Get user statistics"""
        try:
            user = await self.get_user_by_id(user_id)
            if not user:
                return {}
            
            # Count related entities
            chat_sessions_count = len(user.chat_sessions) if user.chat_sessions else 0
            documents_count = len(user.documents) if user.documents else 0
            
            # Calculate total messages
            total_messages = 0
            if user.chat_sessions:
                for session in user.chat_sessions:
                    total_messages += len(session.messages) if session.messages else 0
            
            return {
                "user_id": user.id,
                "email": user.email,
                "chat_sessions_count": chat_sessions_count,
                "documents_count": documents_count,
                "total_messages": total_messages,
                "account_age_days": (datetime.utcnow() - user.created_at).days if user.created_at else 0,
                "last_login": user.last_login.isoformat() if user.last_login else None
            }
            
        except Exception as e:
            logger.error(f"Error getting user stats for {user_id}: {e}")
            return {} 