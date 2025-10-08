from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
from datetime import datetime, timedelta
from sqlalchemy import func
import os

from config import Config
from backend.database import db, User, Transaction, Budget, SavingsGoal, ChatHistory
from backend.auth import login_required, register_user, authenticate_user, create_token
from backend.ai_service import FinanceAIService
from backend.analytics import FinanceAnalytics

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
CORS(app)
db.init_app(app)

# Initialize AI service with Gemini API
ai_service = FinanceAIService(app.config['GEMINI_API_KEY'])

# Create database tables
with app.app_context():
    db.create_all()


# ============ AUTHENTICATION ROUTES ============

@app.route('/api/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.json
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    success, message, user = register_user(username, email, password)
    
    if success:
        session['user_id'] = user.id
        token = create_token(user.id, app.config['JWT_SECRET_KEY'])
        return jsonify({
            'success': True,
            'message': message,
            'user': user.to_dict(),
            'token': token
        }), 201
    else:
        return jsonify({'success': False, 'error': message}), 400


@app.route('/api/login', methods=['POST'])
def login():
    """Login user"""
    data = request.json
    username = data.get('username')
    password = data.get('password')
    
    success, message, user = authenticate_user(username, password)
    
    if success:
        session['user_id'] = user.id
        token = create_token(user.id, app.config['JWT_SECRET_KEY'])
        return jsonify({
            'success': True,
            'message': message,
            'user': user.to_dict(),
            'token': token
        }), 200
    else:
        return jsonify({'success': False, 'error': message}), 401


@app.route('/api/logout', methods=['POST'])
def logout():
    """Logout user"""
    session.pop('user_id', None)
    return jsonify({'success': True, 'message': 'Logged out successfully'}), 200


# ============ TRANSACTION ROUTES ============

@app.route('/api/transactions', methods=['GET'])
@login_required
def get_transactions(user_id):
    """Get all transactions for user"""
    limit = request.args.get('limit', type=int)
    category = request.args.get('category')
    
    query = Transaction.query.filter_by(user_id=user_id)
    
    if category:
        query = query.filter_by(category=category)
    
    query = query.order_by(Transaction.date.desc())
    
    if limit:
        query = query.limit(limit)
    
    transactions = query.all()
    return jsonify({
        'success': True,
        'transactions': [t.to_dict() for t in transactions]
    }), 200


@app.route('/api/transactions', methods=['POST'])
@login_required
def add_transaction(user_id):
    """Add a new transaction"""
    data = request.json
    
    try:
        transaction = Transaction(
            user_id=user_id,
            amount=float(data['amount']),
            category=data['category'],
            description=data.get('description', ''),
            transaction_type=data.get('transaction_type', 'expense'),
            date=datetime.fromisoformat(data['date']) if 'date' in data else datetime.utcnow()
        )
        
        db.session.add(transaction)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Transaction added successfully',
            'transaction': transaction.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/transactions/<int:transaction_id>', methods=['DELETE'])
@login_required
def delete_transaction(user_id, transaction_id):
    """Delete a transaction"""
    transaction = Transaction.query.filter_by(id=transaction_id, user_id=user_id).first()
    
    if not transaction:
        return jsonify({'success': False, 'error': 'Transaction not found'}), 404
    
    db.session.delete(transaction)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Transaction deleted successfully'}), 200


# ============ BUDGET ROUTES ============

@app.route('/api/budgets', methods=['GET'])
@login_required
def get_budgets(user_id):
    """Get all budgets for user with spent amounts"""
    budgets = Budget.query.filter_by(user_id=user_id).all()
    
    budget_data = []
    for budget in budgets:
        # Calculate spent amount based on period
        now = datetime.utcnow()
        
        if budget.period == 'monthly':
            # Current month
            start_date = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        elif budget.period == 'weekly':
            # Current week
            start_date = now - timedelta(days=now.weekday())
        else:  # yearly
            # Current year
            start_date = now.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        
        # Calculate total spent in this category for the period
        spent = db.session.query(func.sum(Transaction.amount)).filter(
            Transaction.user_id == user_id,
            Transaction.category == budget.category,
            Transaction.transaction_type == 'expense',
            Transaction.date >= start_date
        ).scalar() or 0.0
        
        # Add to budget dict
        budget_dict = budget.to_dict()
        budget_dict['spent'] = float(spent)
        budget_data.append(budget_dict)
    
    return jsonify({
        'success': True,
        'budgets': budget_data
    }), 200


@app.route('/api/budgets', methods=['POST'])
@login_required
def add_budget(user_id):
    """Add or update a budget"""
    data = request.json
    
    try:
        # Check if budget exists for this category
        existing_budget = Budget.query.filter_by(
            user_id=user_id,
            category=data['category']
        ).first()
        
        if existing_budget:
            existing_budget.amount = float(data['amount'])
            existing_budget.period = data.get('period', 'monthly')
            existing_budget.updated_at = datetime.utcnow()
            budget = existing_budget
        else:
            budget = Budget(
                user_id=user_id,
                category=data['category'],
                amount=float(data['amount']),
                period=data.get('period', 'monthly')
            )
            db.session.add(budget)
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Budget saved successfully',
            'budget': budget.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/budgets/<int:budget_id>', methods=['DELETE'])
@login_required
def delete_budget(user_id, budget_id):
    """Delete a budget"""
    budget = Budget.query.filter_by(id=budget_id, user_id=user_id).first()
    
    if not budget:
        return jsonify({'success': False, 'error': 'Budget not found'}), 404
    
    db.session.delete(budget)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Budget deleted successfully'}), 200


# ============ SAVINGS GOAL ROUTES ============

@app.route('/api/savings-goals', methods=['GET'])
@login_required
def get_savings_goals(user_id):
    """Get all savings goals for user"""
    goals = SavingsGoal.query.filter_by(user_id=user_id).all()
    return jsonify({
        'success': True,
        'goals': [g.to_dict() for g in goals]
    }), 200


@app.route('/api/savings-goals', methods=['POST'])
@login_required
def add_savings_goal(user_id):
    """Add a new savings goal"""
    data = request.json
    
    try:
        goal = SavingsGoal(
            user_id=user_id,
            name=data['name'],
            target_amount=float(data['target_amount']),
            current_amount=float(data.get('current_amount', 0)),
            deadline=datetime.fromisoformat(data['deadline']) if 'deadline' in data else None
        )
        
        db.session.add(goal)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Savings goal created successfully',
            'goal': goal.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/savings-goals/<int:goal_id>', methods=['PUT'])
@login_required
def update_savings_goal(user_id, goal_id):
    """Update savings goal progress"""
    goal = SavingsGoal.query.filter_by(id=goal_id, user_id=user_id).first()
    
    if not goal:
        return jsonify({'success': False, 'error': 'Goal not found'}), 404
    
    data = request.json
    
    try:
        if 'current_amount' in data:
            goal.current_amount = float(data['current_amount'])
        
        if 'target_amount' in data:
            goal.target_amount = float(data['target_amount'])
        
        if 'name' in data:
            goal.name = data['name']
        
        if 'deadline' in data:
            goal.deadline = datetime.fromisoformat(data['deadline'])
        
        # Check if goal is completed
        if goal.current_amount >= goal.target_amount:
            goal.completed = True
        
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': 'Savings goal updated successfully',
            'goal': goal.to_dict()
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 400


@app.route('/api/savings-goals/<int:goal_id>', methods=['DELETE'])
@login_required
def delete_savings_goal(user_id, goal_id):
    """Delete a savings goal"""
    goal = SavingsGoal.query.filter_by(id=goal_id, user_id=user_id).first()
    
    if not goal:
        return jsonify({'success': False, 'error': 'Goal not found'}), 404
    
    db.session.delete(goal)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Savings goal deleted successfully'}), 200


# ============ AI CHATBOT ROUTES ============

@app.route('/api/chat', methods=['POST'])
@login_required
def chat(user_id):
    """Chat with AI assistant"""
    data = request.json
    message = data.get('message', '')
    
    if not message:
        return jsonify({'success': False, 'error': 'Message is required'}), 400
    
    try:
        # Get user context
        summary = FinanceAnalytics.get_spending_summary(user_id)
        budget_analysis = FinanceAnalytics.get_budget_analysis(user_id)
        savings_progress = FinanceAnalytics.get_savings_progress(user_id)
        
        user_context = {
            'total_expenses': summary['total_expenses'],
            'total_income': summary['total_income'],
            'category_spending': summary['category_spending'],
            'budgets': budget_analysis if budget_analysis['has_budgets'] else {},
            'savings_goals': savings_progress if savings_progress['has_goals'] else {}
        }
        
        # Get AI response
        response = ai_service.get_chatbot_response(message, user_context)
        
        # Save chat history
        chat_history = ChatHistory(
            user_id=user_id,
            message=message,
            response=response
        )
        db.session.add(chat_history)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'response': response
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ============ ANALYTICS ROUTES ============

@app.route('/api/analytics/summary', methods=['GET'])
@login_required
def get_summary(user_id):
    """Get spending summary"""
    period = request.args.get('period', 'month')
    summary = FinanceAnalytics.get_spending_summary(user_id, period)
    return jsonify({'success': True, 'data': summary}), 200


@app.route('/api/analytics/budget-analysis', methods=['GET'])
@login_required
def get_budget_analysis(user_id):
    """Get budget analysis"""
    analysis = FinanceAnalytics.get_budget_analysis(user_id)
    return jsonify({'success': True, 'data': analysis}), 200


@app.route('/api/analytics/savings-progress', methods=['GET'])
@login_required
def get_savings_progress_api(user_id):
    """Get savings progress"""
    progress = FinanceAnalytics.get_savings_progress(user_id)
    return jsonify({'success': True, 'data': progress}), 200


@app.route('/api/analytics/trends', methods=['GET'])
@login_required
def get_trends(user_id):
    """Get spending trends"""
    months = request.args.get('months', 6, type=int)
    trends = FinanceAnalytics.get_spending_trends(user_id, months)
    return jsonify({'success': True, 'data': trends}), 200


@app.route('/api/analytics/categories', methods=['GET'])
@login_required
def get_category_insights(user_id):
    """Get category insights"""
    insights = FinanceAnalytics.get_category_insights(user_id)
    return jsonify({'success': True, 'data': insights}), 200


@app.route('/api/analytics/category-spending', methods=['GET'])
@login_required
def get_category_spending(user_id):
    """Get spending by category for charts"""
    summary = FinanceAnalytics.get_spending_summary(user_id)
    category_data = []
    
    for category, amount in summary['category_spending'].items():
        category_data.append({
            'category': category,
            'amount': amount
        })
    
    return jsonify({'success': True, 'data': category_data}), 200


@app.route('/api/analytics/predictions', methods=['GET'])
@login_required
def get_predictions(user_id):
    """Get expense predictions"""
    transactions = Transaction.query.filter_by(user_id=user_id).all()
    transactions_data = [t.to_dict() for t in transactions]
    
    predictions = ai_service.predict_future_expenses(transactions_data)
    return jsonify({'success': True, 'data': predictions}), 200


@app.route('/api/analytics/suggestions', methods=['GET'])
@login_required
def get_savings_suggestions(user_id):
    """Get savings goal suggestions"""
    summary = FinanceAnalytics.get_spending_summary(user_id)
    suggestions = ai_service.suggest_savings_goals(summary)
    
    # Format suggestions with 'title' field for frontend
    formatted_goals = []
    for suggestion in suggestions:
        formatted_goals.append({
            'title': suggestion['name'],
            'description': suggestion['description'],
            'target_amount': suggestion['target_amount'],
            'suggested_monthly': suggestion['suggested_monthly'],
            'priority': suggestion['priority']
        })
    
    return jsonify({'success': True, 'data': {'goals': formatted_goals}}), 200


# ============ DASHBOARD ROUTE ============

@app.route('/api/dashboard', methods=['GET'])
@login_required
def get_dashboard(user_id):
    """Get dashboard summary data"""
    try:
        # Get spending summary for current month
        summary = FinanceAnalytics.get_spending_summary(user_id, 'month')
        
        # Get total balance (all-time income - all-time expenses)
        all_transactions = Transaction.query.filter_by(user_id=user_id).all()
        total_income = sum(t.amount for t in all_transactions if t.transaction_type == 'income')
        total_expenses = sum(t.amount for t in all_transactions if t.transaction_type == 'expense')
        balance = total_income - total_expenses
        
        # Get goals count
        goals_count = SavingsGoal.query.filter_by(user_id=user_id).count()
        
        return jsonify({
            'success': True,
            'data': {
                'balance': round(balance, 2),
                'month_income': round(summary.get('total_income', 0), 2),
                'month_expenses': round(summary.get('total_expenses', 0), 2),
                'goals_count': goals_count
            }
        }), 200
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


# ============ MAIN PAGE ============

@app.route('/')
def index():
    """Renders the main page"""
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True, port=8080)