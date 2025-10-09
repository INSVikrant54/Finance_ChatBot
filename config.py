import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database configuration - ALWAYS use /tmp for Render (writable location)
    # Check if running on Render or locally
    basedir = os.path.abspath(os.path.dirname(__file__))
    
    # Use /tmp on any cloud platform, instance folder locally
    if os.path.exists('/opt/render'):  # Render detection
        DATABASE_PATH = '/tmp/finance_chatbot.db'
    else:
        # Local development
        instance_path = os.path.join(basedir, 'instance')
        os.makedirs(instance_path, exist_ok=True)
        DATABASE_PATH = os.path.join(instance_path, 'finance_chatbot.db')
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f'sqlite:///{DATABASE_PATH}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-change-in-production'
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY') or 'AIzaSyDOzogpt08zzEDyeQuozXasjXkymljwA0M'
    
    # Session configuration
    PERMANENT_SESSION_LIFETIME = 86400  # 24 hours
    SESSION_COOKIE_SECURE = False  # Changed to False - Render provides HTTPS at proxy level
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SAMESITE = 'Lax'
