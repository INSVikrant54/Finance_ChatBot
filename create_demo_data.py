"""
FinanceAI - Demo Data Script
Creates sample data for demonstration purposes
"""

from app import app, db
from backend.database import User, Transaction, Budget, SavingsGoal
from datetime import datetime, timedelta
import random

def create_demo_data():
    """Create demo user with sample data"""
    
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Check if demo user exists
        demo_user = User.query.filter_by(username='demo').first()
        
        if demo_user:
            print("Demo user already exists!")
            print("Login with: username='demo', password='demo123'")
            return
        
        # Create demo user
        demo_user = User(
            username='demo',
            email='demo@financeai.com'
        )
        demo_user.set_password('demo123')
        db.session.add(demo_user)
        db.session.commit()
        
        print("✅ Created demo user")
        print("   Username: demo")
        print("   Password: demo123")
        
        # Create sample transactions
        today = datetime.utcnow()
        
        # Income transactions
        transactions = [
            Transaction(
                user_id=demo_user.id,
                amount=50000.00,
                category='Salary',
                description='Monthly Salary',
                transaction_type='income',
                date=today - timedelta(days=25)
            ),
            Transaction(
                user_id=demo_user.id,
                amount=15000.00,
                category='Other',
                description='Freelance Project',
                transaction_type='income',
                date=today - timedelta(days=15)
            ),
        ]
        
        # Expense transactions
        expense_data = [
            ('Groceries', 8500, 'Monthly Groceries', 23),
            ('Food & Dining', 3200, 'Restaurant Dinner', 2),
            ('Food & Dining', 1800, 'Lunch', 5),
            ('Transport', 2500, 'Fuel', 10),
            ('Transport', 800, 'Auto Fare', 3),
            ('Utilities', 1500, 'Electricity Bill', 20),
            ('Utilities', 800, 'Internet Bill', 18),
            ('Entertainment', 1200, 'Netflix Subscription', 15),
            ('Entertainment', 1500, 'Movie Night', 7),
            ('Shopping', 4500, 'Clothes Shopping', 12),
            ('Shopping', 2200, 'Electronics', 8),
            ('Healthcare', 1800, 'Doctor Visit', 14),
            ('Education', 3500, 'Online Course', 17),
        ]
        
        for category, amount, desc, days_ago in expense_data:
            transactions.append(
                Transaction(
                    user_id=demo_user.id,
                    amount=amount,
                    category=category,
                    description=desc,
                    transaction_type='expense',
                    date=today - timedelta(days=days_ago)
                )
            )
        
        db.session.add_all(transactions)
        db.session.commit()
        print(f"✅ Created {len(transactions)} sample transactions")
        
        # Create budgets
        budgets = [
            Budget(user_id=demo_user.id, category='Food & Dining', amount=6000, period='monthly'),
            Budget(user_id=demo_user.id, category='Groceries', amount=10000, period='monthly'),
            Budget(user_id=demo_user.id, category='Transport', amount=4000, period='monthly'),
            Budget(user_id=demo_user.id, category='Entertainment', amount=3000, period='monthly'),
            Budget(user_id=demo_user.id, category='Shopping', amount=5000, period='monthly'),
        ]
        
        db.session.add_all(budgets)
        db.session.commit()
        print(f"✅ Created {len(budgets)} sample budgets")
        
        # Create savings goals
        goals = [
            SavingsGoal(
                user_id=demo_user.id,
                name='Emergency Fund',
                target_amount=100000,
                current_amount=45000,
                deadline=today + timedelta(days=180)
            ),
            SavingsGoal(
                user_id=demo_user.id,
                name='Vacation to Goa',
                target_amount=50000,
                current_amount=28000,
                deadline=today + timedelta(days=120)
            ),
            SavingsGoal(
                user_id=demo_user.id,
                name='New Laptop',
                target_amount=80000,
                current_amount=15000,
                deadline=today + timedelta(days=90)
            ),
        ]
        
        db.session.add_all(goals)
        db.session.commit()
        print(f"✅ Created {len(goals)} savings goals")
        
        print("\n" + "="*50)
        print("🎉 Demo data created successfully!")
        print("="*50)
        print("\n📝 Login Credentials:")
        print("   Username: demo")
        print("   Password: demo123")
        print("\n🚀 Start the app with: python app.py")
        print("   Then open: http://localhost:8080")
        print("\n" + "="*50)

if __name__ == '__main__':
    create_demo_data()
