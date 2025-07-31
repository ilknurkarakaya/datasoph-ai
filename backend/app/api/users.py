"""
DATASOPH AI - Users API
User profile management and settings endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
import logging
from datetime import datetime

from app.core.database import get_db
from app.core.security import get_current_user

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/users", tags=["users"])

# Pydantic models
class UserProfile(BaseModel):
    id: int
    email: EmailStr
    name: Optional[str] = None
    picture: Optional[str] = None
    is_active: bool = True
    is_verified: bool = False
    preferred_model: str = "anthropic/claude-3-sonnet"
    theme: str = "light"
    language: str = "en"
    created_at: str
    last_login: Optional[str] = None

class UserProfileUpdate(BaseModel):
    name: Optional[str] = None
    picture: Optional[str] = None
    preferred_model: Optional[str] = None
    theme: Optional[str] = None
    language: Optional[str] = None

class UserSettings(BaseModel):
    notifications: bool = True
    email_updates: bool = True
    data_sharing: bool = False
    analytics_tracking: bool = True

class UserStats(BaseModel):
    total_chats: int
    total_analyses: int
    documents_uploaded: int
    total_usage_hours: float
    account_age_days: int
    last_activity: str

@router.get("/profile", response_model=UserProfile)
async def get_user_profile(
    current_user: Dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get current user's profile information
    """
    try:
        # Mock user profile data
        profile = UserProfile(
            id=1,
            email=current_user.get("email", "user@example.com"),
            name="Demo User",
            picture="https://avatar.example.com/user.jpg",
            is_active=True,
            is_verified=True,
            preferred_model="anthropic/claude-3-sonnet",
            theme="light",
            language="en",
            created_at=datetime.now().isoformat(),
            last_login=datetime.now().isoformat()
        )
        
        return profile
        
    except Exception as e:
        logger.error(f"Error getting user profile: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user profile"
        )

@router.put("/profile", response_model=UserProfile)
async def update_user_profile(
    profile_update: UserProfileUpdate,
    current_user: Dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update user profile information
    """
    try:
        # Mock profile update
        updated_profile = UserProfile(
            id=1,
            email=current_user.get("email", "user@example.com"),
            name=profile_update.name or "Demo User",
            picture=profile_update.picture or "https://avatar.example.com/user.jpg",
            is_active=True,
            is_verified=True,
            preferred_model=profile_update.preferred_model or "anthropic/claude-3-sonnet",
            theme=profile_update.theme or "light",
            language=profile_update.language or "en",
            created_at=datetime.now().isoformat(),
            last_login=datetime.now().isoformat()
        )
        
        return updated_profile
        
    except Exception as e:
        logger.error(f"Error updating user profile: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user profile"
        )

@router.get("/settings", response_model=UserSettings)
async def get_user_settings(
    current_user: Dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user's application settings
    """
    try:
        # Mock user settings
        settings = UserSettings(
            notifications=True,
            email_updates=True,
            data_sharing=False,
            analytics_tracking=True
        )
        
        return settings
        
    except Exception as e:
        logger.error(f"Error getting user settings: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user settings"
        )

@router.put("/settings", response_model=UserSettings)
async def update_user_settings(
    settings_update: UserSettings,
    current_user: Dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update user's application settings
    """
    try:
        # Mock settings update
        return settings_update
        
    except Exception as e:
        logger.error(f"Error updating user settings: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update user settings"
        )

@router.get("/stats", response_model=UserStats)
async def get_user_stats(
    current_user: Dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user's usage statistics
    """
    try:
        # Mock user statistics
        stats = UserStats(
            total_chats=47,
            total_analyses=23,
            documents_uploaded=12,
            total_usage_hours=38.5,
            account_age_days=45,
            last_activity=datetime.now().isoformat()
        )
        
        return stats
        
    except Exception as e:
        logger.error(f"Error getting user stats: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user statistics"
        )

@router.get("/activity")
async def get_user_activity(
    limit: int = 10,
    current_user: Dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Get user's recent activity
    """
    try:
        # Mock activity data
        activities = [
            {
                "id": "activity_1",
                "type": "chat",
                "description": "Started new chat session about data analysis",
                "timestamp": datetime.now().isoformat()
            },
            {
                "id": "activity_2",
                "type": "analysis",
                "description": "Analyzed sales_data.csv dataset",
                "timestamp": datetime.now().isoformat()
            },
            {
                "id": "activity_3",
                "type": "document",
                "description": "Uploaded research_paper.pdf to RAG system",
                "timestamp": datetime.now().isoformat()
            },
            {
                "id": "activity_4",
                "type": "chat",
                "description": "Queried documents about machine learning",
                "timestamp": datetime.now().isoformat()
            }
        ]
        
        return {
            "activities": activities[:limit],
            "total": len(activities)
        }
        
    except Exception as e:
        logger.error(f"Error getting user activity: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve user activity"
        )

@router.delete("/account")
async def delete_user_account(
    current_user: Dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Delete user account (soft delete)
    """
    try:
        return {
            "message": "Account deletion request received. Your account will be deactivated within 24 hours.",
            "deletion_scheduled": True
        }
        
    except Exception as e:
        logger.error(f"Error deleting user account: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process account deletion"
        )

@router.post("/export-data")
async def export_user_data(
    current_user: Dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Export user's data (GDPR compliance)
    """
    try:
        return {
            "message": "Data export request received. You will receive a download link via email within 24 hours.",
            "export_scheduled": True,
            "estimated_completion": datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error exporting user data: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process data export request"
        )

@router.get("/health")
async def users_health():
    """Users service health check"""
    return {
        "status": "healthy",
        "service": "users",
        "timestamp": datetime.now().isoformat()
    } 