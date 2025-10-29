"""
Authentication models for user management and JWT authentication.
"""
import uuid
import bcrypt
from datetime import datetime


class User:
    """User model for authentication."""
    
    def __init__(self, username, password_hash, user_id=None, created_at=None):
        """
        Initialize a user.
        
        Args:
            username: Username for the user
            password_hash: Hashed password
            user_id: Unique identifier (generated if not provided)
            created_at: Creation timestamp
        """
        self.user_id = user_id if user_id else str(uuid.uuid4())
        self.username = username
        self.password_hash = password_hash
        self.created_at = created_at if created_at else datetime.now()
    
    @staticmethod
    def hash_password(password):
        """Hash a password using bcrypt."""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def verify_password(self, password):
        """Verify a password against the stored hash."""
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
    
    def to_dict(self):
        """Convert user to dictionary for JSON serialization."""
        return {
            'user_id': self.user_id,
            'username': self.username,
            'password_hash': self.password_hash,
            'created_at': self.created_at.isoformat() if isinstance(self.created_at, datetime) else self.created_at
        }
    
    @classmethod
    def from_dict(cls, data):
        """Create a User instance from a dictionary."""
        created_at = data.get('created_at')
        if created_at and isinstance(created_at, str):
            created_at = datetime.fromisoformat(created_at)
        
        return cls(
            username=data['username'],
            password_hash=data['password_hash'],
            user_id=data.get('user_id'),
            created_at=created_at
        )
