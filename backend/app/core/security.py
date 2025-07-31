"""
DATASOPH AI - Security Module
JWT Token Management and Firebase Authentication
"""

from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import firebase_admin
from firebase_admin import auth, credentials
import logging

from app.core.config import settings

logger = logging.getLogger(__name__)

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# HTTP Bearer for JWT tokens
security = HTTPBearer()

# Initialize Firebase Admin SDK
def initialize_firebase():
    """Initialize Firebase Admin SDK"""
    try:
        if not firebase_admin._apps:
            # Initialize with credentials from environment
            if settings.FIREBASE_PROJECT_ID:
                cred = credentials.Certificate(settings.firebase_credentials)
                firebase_admin.initialize_app(cred)
                logger.info("✅ Firebase Admin SDK initialized successfully")
            else:
                logger.warning("⚠️ Firebase credentials not configured")
    except Exception as e:
        logger.error(f"❌ Failed to initialize Firebase: {e}")

# Initialize Firebase on import
initialize_firebase()

class JWTManager:
    """JWT Token Management"""
    
    def __init__(self):
        self.secret_key = settings.SECRET_KEY
        self.algorithm = settings.ALGORITHM
        self.access_token_expire_minutes = settings.ACCESS_TOKEN_EXPIRE_MINUTES
        self.refresh_token_expire_days = settings.REFRESH_TOKEN_EXPIRE_DAYS
    
    def create_access_token(self, user_id: str, email: str, **extra_claims) -> str:
        """Create JWT access token"""
        expire = datetime.utcnow() + timedelta(minutes=self.access_token_expire_minutes)
        payload = {
            "user_id": user_id,
            "email": email,
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "access",
            **extra_claims
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    def create_refresh_token(self, user_id: str) -> str:
        """Create JWT refresh token"""
        expire = datetime.utcnow() + timedelta(days=self.refresh_token_expire_days)
        payload = {
            "user_id": user_id,
            "exp": expire,
            "iat": datetime.utcnow(),
            "type": "refresh"
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
    
    def verify_token(self, token: str) -> Dict[str, Any]:
        """Verify and decode JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError as e:
            logger.error(f"JWT verification failed: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    def verify_refresh_token(self, refresh_token: str) -> Dict[str, Any]:
        """Verify refresh token"""
        payload = self.verify_token(refresh_token)
        if payload.get("type") != "refresh":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid refresh token type"
            )
        return payload

class FirebaseAuth:
    """Firebase Authentication Management"""
    
    @staticmethod
    async def verify_firebase_token(firebase_token: str) -> Dict[str, Any]:
        """Verify Firebase ID token"""
        try:
            decoded_token = auth.verify_id_token(firebase_token)
            return {
                "uid": decoded_token["uid"],
                "email": decoded_token.get("email"),
                "name": decoded_token.get("name"),
                "picture": decoded_token.get("picture"),
                "email_verified": decoded_token.get("email_verified", False),
                "firebase_claims": decoded_token
            }
        except Exception as e:
            logger.error(f"Firebase token verification failed: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Firebase token"
            )
    
    @staticmethod
    async def create_custom_token(uid: str, additional_claims: Optional[Dict] = None) -> str:
        """Create Firebase custom token"""
        try:
            return auth.create_custom_token(uid, additional_claims)
        except Exception as e:
            logger.error(f"Failed to create custom token: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create custom token"
            )

# Initialize managers
jwt_manager = JWTManager()
firebase_auth = FirebaseAuth()

# Password utilities
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash a password"""
    return pwd_context.hash(password)

# Dependency for protected routes
async def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """Dependency to verify JWT token for protected routes"""
    token = credentials.credentials
    payload = jwt_manager.verify_token(token)
    
    # Additional validation
    if payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type"
        )
    
    return payload

async def get_current_user(token_payload: Dict = Depends(verify_token)) -> Dict[str, Any]:
    """Get current user from token payload"""
    return {
        "user_id": token_payload["user_id"],
        "email": token_payload["email"]
    }

# Optional dependency (doesn't raise error if no token)
async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(HTTPBearer(auto_error=False))
) -> Optional[Dict[str, Any]]:
    """Optional user dependency that doesn't fail if no token provided"""
    if not credentials:
        return None
    
    try:
        payload = jwt_manager.verify_token(credentials.credentials)
        return {
            "user_id": payload["user_id"],
            "email": payload["email"]
        }
    except HTTPException:
        return None 