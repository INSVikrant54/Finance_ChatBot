#!/usr/bin/env python3
"""
Pre-Deployment Verification Script
Run this before deploying to check for common issues
"""

import os
import sys

def check_requirements():
    """Check if requirements.txt exists and is valid"""
    print("🔍 Checking requirements.txt...")
    if not os.path.exists('requirements.txt'):
        print("❌ requirements.txt not found!")
        return False
    
    with open('requirements.txt', 'r') as f:
        lines = f.readlines()
        
    # Check for problematic packages
    problematic = ['pandas', 'numpy', 'scikit-learn', 'jwt==']
    for line in lines:
        for pkg in problematic:
            if pkg in line.lower():
                print(f"⚠️  WARNING: Found problematic package: {line.strip()}")
    
    print("✅ requirements.txt OK")
    return True

def check_procfile():
    """Check if Procfile exists"""
    print("\n🔍 Checking Procfile...")
    if not os.path.exists('Procfile'):
        print("❌ Procfile not found!")
        return False
    
    with open('Procfile', 'r') as f:
        content = f.read()
    
    if 'gunicorn app:app' not in content:
        print(f"⚠️  WARNING: Procfile doesn't contain 'gunicorn app:app': {content}")
    
    print("✅ Procfile OK")
    return True

def check_runtime():
    """Check if runtime.txt exists"""
    print("\n🔍 Checking runtime.txt...")
    if not os.path.exists('runtime.txt'):
        print("⚠️  runtime.txt not found (optional)")
        return True
    
    with open('runtime.txt', 'r') as f:
        content = f.read().strip()
    
    print(f"   Python version: {content}")
    print("✅ runtime.txt OK")
    return True

def check_config():
    """Check if config.py has proper database configuration"""
    print("\n🔍 Checking config.py...")
    if not os.path.exists('config.py'):
        print("❌ config.py not found!")
        return False
    
    with open('config.py', 'r') as f:
        content = f.read()
    
    if '/tmp/finance_chatbot.db' not in content:
        print("⚠️  WARNING: config.py doesn't use /tmp for database")
    
    if '/opt/render' in content:
        print("✅ config.py has Render detection")
    
    print("✅ config.py OK")
    return True

def check_app():
    """Check if app.py exists and imports correctly"""
    print("\n🔍 Checking app.py...")
    if not os.path.exists('app.py'):
        print("❌ app.py not found!")
        return False
    
    try:
        # Try importing config
        from config import Config
        print(f"   Database URI: {Config.SQLALCHEMY_DATABASE_URI}")
        print("✅ app.py and config import OK")
        return True
    except Exception as e:
        print(f"❌ Error importing: {e}")
        return False

def check_gitignore():
    """Check if sensitive files are ignored"""
    print("\n🔍 Checking .gitignore...")
    if not os.path.exists('.gitignore'):
        print("⚠️  .gitignore not found")
        return True
    
    with open('.gitignore', 'r') as f:
        content = f.read()
    
    required = ['.env', '*.db', '__pycache__']
    for item in required:
        if item not in content:
            print(f"⚠️  WARNING: {item} not in .gitignore")
    
    print("✅ .gitignore OK")
    return True

def main():
    print("="*60)
    print(" 🚀 PRE-DEPLOYMENT VERIFICATION")
    print("="*60)
    
    checks = [
        check_requirements,
        check_procfile,
        check_runtime,
        check_config,
        check_app,
        check_gitignore
    ]
    
    results = []
    for check in checks:
        try:
            results.append(check())
        except Exception as e:
            print(f"❌ Check failed: {e}")
            results.append(False)
    
    print("\n" + "="*60)
    if all(results):
        print("✅ ALL CHECKS PASSED! Ready for deployment!")
        print("="*60)
        return 0
    else:
        print("⚠️  SOME CHECKS FAILED! Fix issues before deploying.")
        print("="*60)
        return 1

if __name__ == "__main__":
    sys.exit(main())
