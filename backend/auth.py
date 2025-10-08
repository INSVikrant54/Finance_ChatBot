from functools import wraps
from flask import request, jsonify, session
import jwt
from datetime import datetime, timedelta
from backend.database import User, db

def create_token(user_id: int, secret_key: str) -> str:
    """Create JWT token for user"""
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, secret_key, algorithm='HS256')

def verify_token(token: str, secret_key: str) -> dict:
    """Verify JWT token"""
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def login_required(f):
    """Decorator to require login for routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Check session first
        user_id = session.get('user_id')
        if user_id:
            return f(user_id=user_id, *args, **kwargs)
        
        # Check Authorization header
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({'error': 'No authorization token provided'}), 401
        
        try:
            token = auth_header.split(' ')[1]  # Bearer <token>
            from flask import current_app
            payload = verify_token(token, current_app.config['JWT_SECRET_KEY'])
            
            if not payload:
                return jsonify({'error': 'Invalid or expired token'}), 401
            
            return f(user_id=payload['user_id'], *args, **kwargs)
        
        except Exception as e:
            return jsonify({'error': 'Invalid authorization header'}), 401
    
    return decorated_function

def register_user(username: str, email: str, password: str) -> tuple:
    """
    Register a new user
    
    Returns:
        (success: bool, message: str, user: User or None)
    """
    # Validate input
    if not username or not email or not password:
        return False, 'All fields are required', None
    
    if len(password) < 6:
        return False, 'Password must be at least 6 characters', None
    
    # Check if user exists
    existing_user = User.query.filter(
        (User.username == username) | (User.email == email)
    ).first()
    
    if existing_user:
        return False, 'Username or email already exists', None
    
    # Create new user
    try:
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return True, 'User registered successfully', user
    except Exception as e:
        db.session.rollback()
        return False, f'Error registering user: {str(e)}', None

def authenticate_user(username: str, password: str) -> tuple:
    """
    Authenticate a user
    
    Returns:
        (success: bool, message: str, user: User or None)
    """
    if not username or not password:
        return False, 'Username and password are required', None
    
    # Find user
    user = User.query.filter_by(username=username).first()
    
    if not user or not user.check_password(password):
        return False, 'Invalid username or password', None
    
    return True, 'Login successful', user
