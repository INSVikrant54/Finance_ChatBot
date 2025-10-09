import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database configuration - use /opt/render/project/data for Render persistence
    # or /tmp for temporary storage on Render free tier
    if os.environ.get('RENDER'):
        # On Render, use absolute path to /tmp (Render free tier)
        DATABASE_PATH = '/tmp/finance_chatbot.db'
    else:
        # Local development
        basedir = os.path.abspath(os.path.dirname(__file__))
        DATABASE_PATH = os.path.join(basedir, 'instance', 'finance_chatbot.db')
        # Create instance directory if it doesn't exist
        os.makedirs(os.path.dirname(DATABASE_PATH), exist_ok=True)
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f'sqlite:///{DATABASE_PATH}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-change-in-production'
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY') or 'AIzaSyDOzogpt08zzEDyeQuozXasjXkymljwA0M'
    
    # Session configuration
    PERMANENT_SESSION_LIFETIME = 86400  # 24 hours
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
