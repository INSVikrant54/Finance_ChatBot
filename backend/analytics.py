from datetime import datetime, timedelta
from typing import Dict, List
from sqlalchemy import func
from backend.database import Transaction, Budget, SavingsGoal, db

class FinanceAnalytics:
    """Analytics service for financial data"""
    
    @staticmethod
    def get_spending_summary(user_id: int, period: str = 'month') -> Dict:
        """
        Get spending summary for a period
        
        Args:
            user_id: User ID
            period: 'week', 'month', or 'year'
        
        Returns:
            Dictionary with spending summary
        """
        # Calculate date range
        now = datetime.utcnow()
        if period == 'week':
            start_date = now - timedelta(days=7)
        elif period == 'year':
            start_date = now - timedelta(days=365)
        else:  # month
            start_date = now - timedelta(days=30)
        
        # Query transactions
        transactions = Transaction.query.filter(
            Transaction.user_id == user_id,
            Transaction.date >= start_date
        ).all()
        
        # Calculate totals
        total_expenses = sum(t.amount for t in transactions if t.transaction_type == 'expense')
        total_income = sum(t.amount for t in transactions if t.transaction_type == 'income')
        
        # Category breakdown
        category_spending = {}
        for t in transactions:
            if t.transaction_type == 'expense':
                category_spending[t.category] = category_spending.get(t.category, 0) + t.amount
        
        # Get budget information for health score calculation
        budgets = Budget.query.filter_by(user_id=user_id).all()
        budget_data = []
        for budget in budgets:
            spent = category_spending.get(budget.category, 0)
            budget_data.append({
                'category': budget.category,
                'amount': budget.amount,
                'spent': round(spent, 2)
            })
        
        return {
            'period': period,
            'start_date': start_date.isoformat(),
            'end_date': now.isoformat(),
            'total_expenses': round(total_expenses, 2),
            'total_income': round(total_income, 2),
            'income': round(total_income, 2),
            'expenses': round(total_expenses, 2),
            'net_savings': round(total_income - total_expenses, 2),
            'category_spending': {k: round(v, 2) for k, v in category_spending.items()},
            'transaction_count': len(transactions),
            'budgets': budget_data
        }
    
    @staticmethod
    def get_budget_analysis(user_id: int) -> Dict:
        """
        Analyze budget vs actual spending
        
        Args:
            user_id: User ID
        
        Returns:
            Dictionary with budget analysis
        """
        budgets = Budget.query.filter_by(user_id=user_id).all()
        
        if not budgets:
            return {
                'has_budgets': False,
                'message': 'No budgets set yet'
            }
        
        # Get current month spending
        now = datetime.utcnow()
        start_of_month = datetime(now.year, now.month, 1)
        
        transactions = Transaction.query.filter(
            Transaction.user_id == user_id,
            Transaction.date >= start_of_month,
            Transaction.transaction_type == 'expense'
        ).all()
        
        # Calculate spending by category
        category_spending = {}
        for t in transactions:
            category_spending[t.category] = category_spending.get(t.category, 0) + t.amount
        
        # Compare with budgets
        budget_analysis = []
        for budget in budgets:
            spent = category_spending.get(budget.category, 0)
            remaining = budget.amount - spent
            percentage = (spent / budget.amount * 100) if budget.amount > 0 else 0
            
            status = 'on_track'
            if percentage >= 100:
                status = 'exceeded'
            elif percentage >= 80:
                status = 'warning'
            
            budget_analysis.append({
                'category': budget.category,
                'budget': budget.amount,
                'spent': round(spent, 2),
                'remaining': round(remaining, 2),
                'percentage': round(percentage, 1),
                'status': status
            })
        
        return {
            'has_budgets': True,
            'budgets': budget_analysis,
            'total_budget': sum(b.amount for b in budgets),
            'total_spent': sum(category_spending.values()),
            'month': now.strftime('%B %Y')
        }
    
    @staticmethod
    def get_savings_progress(user_id: int) -> Dict:
        """
        Get savings goals progress
        
        Args:
            user_id: User ID
        
        Returns:
            Dictionary with savings progress
        """
        goals = SavingsGoal.query.filter_by(user_id=user_id, completed=False).all()
        
        if not goals:
            return {
                'has_goals': False,
                'message': 'No savings goals set yet'
            }
        
        goals_data = []
        for goal in goals:
            progress = (goal.current_amount / goal.target_amount * 100) if goal.target_amount > 0 else 0
            remaining = goal.target_amount - goal.current_amount
            
            # Calculate days remaining
            days_remaining = None
            if goal.deadline:
                days_remaining = (goal.deadline - datetime.utcnow()).days
            
            goals_data.append({
                'id': goal.id,
                'name': goal.name,
                'target_amount': goal.target_amount,
                'current_amount': goal.current_amount,
                'remaining': round(remaining, 2),
                'progress': round(progress, 1),
                'deadline': goal.deadline.isoformat() if goal.deadline else None,
                'days_remaining': days_remaining
            })
        
        return {
            'has_goals': True,
            'goals': goals_data,
            'total_target': sum(g.target_amount for g in goals),
            'total_saved': sum(g.current_amount for g in goals)
        }
    
    @staticmethod
    def get_spending_trends(user_id: int, months: int = 6) -> list:
        """
        Get spending trends over time with both expenses and income
        
        Args:
            user_id: User ID
            months: Number of months to analyze
        
        Returns:
            List of monthly data with expenses and income
        """
        now = datetime.utcnow()
        start_date = now - timedelta(days=months * 30)
        
        # Get all transactions
        transactions = Transaction.query.filter(
            Transaction.user_id == user_id,
            Transaction.date >= start_date
        ).all()
        
        # Group by month
        monthly_data = {}
        for t in transactions:
            month_key = t.date.strftime('%b %Y')  # Format: "Oct 2025"
            if month_key not in monthly_data:
                monthly_data[month_key] = {'expenses': 0, 'income': 0}
            
            if t.transaction_type == 'expense':
                monthly_data[month_key]['expenses'] += t.amount
            else:  # income
                monthly_data[month_key]['income'] += t.amount
        
        # Sort by date and format for frontend
        sorted_data = []
        for i in range(months):
            date = now - timedelta(days=(months - i - 1) * 30)
            month_key = date.strftime('%b %Y')
            
            sorted_data.append({
                'month': month_key,
                'expenses': round(monthly_data.get(month_key, {}).get('expenses', 0), 2),
                'income': round(monthly_data.get(month_key, {}).get('income', 0), 2)
            })
        
        return sorted_data
    
    @staticmethod
    def get_category_insights(user_id: int) -> Dict:
        """
        Get insights about spending categories
        
        Args:
            user_id: User ID
        
        Returns:
            Dictionary with category insights
        """
        # Get last 30 days transactions
        now = datetime.utcnow()
        start_date = now - timedelta(days=30)
        
        transactions = Transaction.query.filter(
            Transaction.user_id == user_id,
            Transaction.date >= start_date,
            Transaction.transaction_type == 'expense'
        ).all()
        
        if not transactions:
            return {
                'has_data': False,
                'message': 'No transaction data available'
            }
        
        # Category analysis
        category_data = {}
        total_spending = 0
        
        for t in transactions:
            category = t.category
            if category not in category_data:
                category_data[category] = {
                    'total': 0,
                    'count': 0,
                    'transactions': []
                }
            
            category_data[category]['total'] += t.amount
            category_data[category]['count'] += 1
            category_data[category]['transactions'].append(t.amount)
            total_spending += t.amount
        
        # Calculate insights
        insights = []
        for category, data in category_data.items():
            percentage = (data['total'] / total_spending * 100) if total_spending > 0 else 0
            avg_transaction = data['total'] / data['count']
            
            insights.append({
                'category': category,
                'total': round(data['total'], 2),
                'percentage': round(percentage, 1),
                'transaction_count': data['count'],
                'average_transaction': round(avg_transaction, 2)
            })
        
        # Sort by total spending
        insights.sort(key=lambda x: x['total'], reverse=True)
        
        return {
            'has_data': True,
            'categories': insights,
            'total_spending': round(total_spending, 2),
            'period_days': 30
        }
