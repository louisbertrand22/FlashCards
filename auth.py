"""
Authentication routes and JWT management for the Flashcard application.
"""
import os
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from user_manager import UserManager

auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# Configure data directory for user storage
data_dir = os.environ.get('FLASHCARD_DATA_DIR', '.')
if not os.path.exists(data_dir):
    os.makedirs(data_dir)
user_storage_file = os.path.join(data_dir, 'users.json')

# Initialize user manager
user_manager = UserManager(storage_file=user_storage_file)


@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user.
    
    Expected JSON body:
    {
        "username": "user123",
        "password": "password123"
    }
    
    Returns:
        JSON response with user_id and message
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Invalid request body'}), 400
    
    username = data.get('username', '').strip()
    password = data.get('password', '')
    
    # Validation
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    
    if len(username) < 3:
        return jsonify({'error': 'Username must be at least 3 characters long'}), 400
    
    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters long'}), 400
    
    # Create user
    user = user_manager.create_user(username, password)
    
    if not user:
        return jsonify({'error': 'Username already exists'}), 409
    
    return jsonify({
        'message': 'User registered successfully',
        'user_id': user.user_id,
        'username': user.username
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Authenticate a user and return JWT tokens.
    
    Expected JSON body:
    {
        "username": "user123",
        "password": "password123"
    }
    
    Returns:
        JSON response with access_token and refresh_token
    """
    data = request.get_json()
    
    if not data:
        return jsonify({'error': 'Invalid request body'}), 400
    
    username = data.get('username', '').strip()
    password = data.get('password', '')
    
    if not username or not password:
        return jsonify({'error': 'Username and password are required'}), 400
    
    # Authenticate user
    user = user_manager.authenticate_user(username, password)
    
    if not user:
        return jsonify({'error': 'Invalid username or password'}), 401
    
    # Create JWT tokens
    access_token = create_access_token(identity=user.user_id)
    refresh_token = create_refresh_token(identity=user.user_id)
    
    return jsonify({
        'message': 'Login successful',
        'access_token': access_token,
        'refresh_token': refresh_token,
        'user_id': user.user_id,
        'username': user.username
    }), 200


@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """
    Refresh an access token using a refresh token.
    
    Requires a valid refresh token in the Authorization header.
    
    Returns:
        JSON response with new access_token
    """
    current_user_id = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user_id)
    
    return jsonify({
        'access_token': new_access_token
    }), 200


@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """
    Get the current authenticated user's information.
    
    Requires a valid access token in the Authorization header.
    
    Returns:
        JSON response with user information
    """
    current_user_id = get_jwt_identity()
    user = user_manager.get_user_by_id(current_user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    return jsonify({
        'user_id': user.user_id,
        'username': user.username,
        'created_at': user.created_at.isoformat() if hasattr(user.created_at, 'isoformat') else user.created_at
    }), 200
