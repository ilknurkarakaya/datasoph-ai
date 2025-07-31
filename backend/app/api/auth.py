"""
DATASOPH AI - Authentication API
Firebase + JWT Authentication endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from typing import Optional
import logging
from datetime import datetime

from app.core.database import get_db
from app.core.security import jwt_manager, firebase_auth, security
from app.services.user_service import UserService
from app.models.user import User

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/auth", tags=["authentication"])

# Pydantic models for requests and responses
class FirebaseLoginRequest(BaseModel):
    firebase_token: str

class LoginResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: dict

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserProfileResponse(BaseModel):
    id: int
    email: str
    name: Optional[str]
    picture: Optional[str]
    is_active: bool
    is_verified: bool
    preferred_model: str
    theme: str
    language: str
    created_at: str
    last_login: Optional[str]

@router.post("/firebase-login", response_model=LoginResponse)
async def firebase_login(
    request: FirebaseLoginRequest,
    db: Session = Depends(get_db)
):
    """
    Authenticate user with Firebase token and return JWT tokens
    """
    try:
        # Verify Firebase token
        firebase_user = await firebase_auth.verify_firebase_token(request.firebase_token)
        
        logger.info(f"Firebase user authenticated: {firebase_user['email']}")
        
        # Create or get user in our database
        user_service = UserService(db)
        user = await user_service.create_or_get_user(
            firebase_uid=firebase_user['uid'],
            email=firebase_user['email'],
            name=firebase_user.get('name'),
            picture=firebase_user.get('picture')
        )
        
        # Update last login
        await user_service.update_last_login(user.id)
        
        # Generate JWT tokens
        access_token = jwt_manager.create_access_token(
            user_id=str(user.id),
            email=user.email
        )
        refresh_token = jwt_manager.create_refresh_token(user_id=str(user.id))
        
        logger.info(f"JWT tokens generated for user: {user.email}")
        
        return LoginResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user=user.to_dict()
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Firebase login failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Authentication failed"
        )

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    request: RefreshTokenRequest,
    db: Session = Depends(get_db)
):
    """
    Refresh access token using refresh token
    """
    try:
        # Verify refresh token
        payload = jwt_manager.verify_refresh_token(request.refresh_token)
        
        # Get user from database
        user_service = UserService(db)
        user = await user_service.get_user_by_id(int(payload["user_id"]))
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Generate new access token
        access_token = jwt_manager.create_access_token(
            user_id=str(user.id),
            email=user.email
        )
        
        logger.info(f"Access token refreshed for user: {user.email}")
        
        return TokenResponse(access_token=access_token)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Token refresh failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Token refresh failed"
        )

@router.post("/logout")
async def logout():
    """
    Logout endpoint (client should remove tokens)
    """
    return {"message": "Logged out successfully"}

@router.get("/me", response_model=UserProfileResponse)
async def get_current_user_profile(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    """
    Get current user profile information
    """
    try:
        # Verify token
        payload = jwt_manager.verify_token(credentials.credentials)
        
        # Get user from database
        user_service = UserService(db)
        user = await user_service.get_user_by_id(int(payload["user_id"]))
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        return UserProfileResponse(**user.to_dict())
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get user profile failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get user profile"
        )

@router.get("/verify-token")
async def verify_token_endpoint(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Verify if the provided token is valid
    """
    try:
        payload = jwt_manager.verify_token(credentials.credentials)
        return {
            "valid": True,
            "user_id": payload["user_id"],
            "email": payload["email"],
            "exp": payload["exp"]
        }
    except HTTPException:
        return {"valid": False}

@router.get("/firebase-config")
async def get_firebase_config():
    """
    Get Firebase configuration for frontend
    """
    from app.core.config import settings
    
    return {
        "project_id": settings.FIREBASE_PROJECT_ID,
        "auth_domain": f"{settings.FIREBASE_PROJECT_ID}.firebaseapp.com",
        "api_key": "your-firebase-web-api-key",  # This should come from frontend config
        "messaging_sender_id": settings.FIREBASE_CLIENT_ID
    } 