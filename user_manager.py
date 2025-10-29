"""
User manager for handling user authentication and storage.
"""
import os
import json
from auth_models import User


class UserManager:
    """Manager for user operations."""
    
    def __init__(self, storage_file='users.json'):
        """
        Initialize the user manager.
        
        Args:
            storage_file: Path to the JSON file for storing users
        """
        self.storage_file = storage_file
        self.users = self._load_users()
    
    def _load_users(self):
        """Load users from the storage file."""
        if not os.path.exists(self.storage_file):
            return {}
        
        try:
            with open(self.storage_file, 'r') as f:
                data = json.load(f)
                return {username: User.from_dict(user_data) 
                        for username, user_data in data.items()}
        except json.JSONDecodeError:
            return {}
        except PermissionError:
            print(f"Error: Permission denied when trying to read from {self.storage_file}")
            print("Please check file permissions.")
            return {}
        except OSError as e:
            print(f"Error: Could not load users from {self.storage_file}: {e}")
            return {}
    
    def _save_users(self):
        """Save users to the storage file."""
        try:
            data = {username: user.to_dict() 
                    for username, user in self.users.items()}
            
            with open(self.storage_file, 'w') as f:
                json.dump(data, f, indent=2)
        except PermissionError:
            print(f"Error: Permission denied when trying to write to {self.storage_file}")
            print("Please check file permissions or choose a different location.")
        except OSError as e:
            print(f"Error: Could not save users to {self.storage_file}: {e}")
            print("Please check that the directory exists and is writable.")
    
    def create_user(self, username, password):
        """
        Create a new user.
        
        Args:
            username: Username for the new user
            password: Plain text password
            
        Returns:
            User object if successful, None if username already exists
        """
        if username in self.users:
            return None
        
        password_hash = User.hash_password(password)
        user = User(username=username, password_hash=password_hash)
        self.users[username] = user
        self._save_users()
        return user
    
    def get_user(self, username):
        """
        Get a user by username.
        
        Args:
            username: Username to look up
            
        Returns:
            User object if found, None otherwise
        """
        return self.users.get(username)
    
    def authenticate_user(self, username, password):
        """
        Authenticate a user with username and password.
        
        Args:
            username: Username
            password: Plain text password
            
        Returns:
            User object if authentication successful, None otherwise
        """
        user = self.get_user(username)
        if user and user.verify_password(password):
            return user
        return None
    
    def get_user_by_id(self, user_id):
        """
        Get a user by user ID.
        
        Args:
            user_id: User ID to look up
            
        Returns:
            User object if found, None otherwise
        """
        for user in self.users.values():
            if user.user_id == user_id:
                return user
        return None
