try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("Google Generative AI module not installed. Using fallback responses.")

from datetime import datetime, timedelta
from typing import Dict, List
import json

class FinanceAIService:
    """AI Service for financial advice and predictions"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.model = None
        if api_key and GEMINI_AVAILABLE:
            genai.configure(api_key=api_key)
            # Use gemini-2.0-flash which is fast and available
            self.model = genai.GenerativeModel('gemini-2.0-flash')
    
    def get_chatbot_response(self, message: str, user_context: Dict) -> str:
        """
        Get AI chatbot response based on user message and context
        
        Args:
            message: User's message
            user_context: Dictionary containing user's financial data
        
        Returns:
            AI-generated response
        """
        if not self.api_key or not GEMINI_AVAILABLE:
            return self._get_fallback_response(message, user_context)
        
        try:
            # Build context from user data
            context = self._build_context(user_context)
            
            # Create optimized system prompt
            system_prompt = """You are FinanceAI, a smart financial advisor who gives laser-focused advice.

STRICT RULES:
- Maximum 50 words per response
- Give 1-2 actionable tips only
- Use bullet points (•) for clarity
- Skip greetings and fluff
- Be direct and specific
- Use numbers when relevant
- One emoji max (optional)
- Focus on the user's actual question

Examples:
Q: "How to save money?"
A: "• Save 20% of income automatically
• Cut one unnecessary subscription
• Cook 3 meals/week at home
Track progress weekly!"

Q: "My expenses are high"
A: "Your top spending: Food ₹5,000
• Try meal prep (save ₹2,000)
• Set ₹4,000 monthly limit
Review in 2 weeks!"

Be precise, actionable, and brief."""
            
            # Combine system prompt with user message and context
            full_prompt = f"""{system_prompt}

User's Financial Data:
{context}

User's Question: {message}

Your Response (max 50 words, bullet points):"""
            
            # Make API call to Gemini
            response = self.model.generate_content(full_prompt)
            
            return response.text.strip()
        
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
            return self._get_fallback_response(message, user_context)
    
    def _build_context(self, user_context: Dict) -> str:
        """Build context string from user data"""
        context_parts = []
        
        if 'total_expenses' in user_context:
            context_parts.append(f"Total Expenses: ₹{user_context['total_expenses']:.2f}")
        
        if 'total_income' in user_context:
            context_parts.append(f"Total Income: ₹{user_context['total_income']:.2f}")
        
        if 'category_spending' in user_context:
            context_parts.append(f"Spending by Category: {user_context['category_spending']}")
        
        if 'budgets' in user_context:
            context_parts.append(f"Active Budgets: {user_context['budgets']}")
        
        if 'savings_goals' in user_context:
            context_parts.append(f"Savings Goals: {user_context['savings_goals']}")
        
        return "\n".join(context_parts)
    
    def _get_fallback_response(self, message: str, user_context: Dict) -> str:
        """Optimized fallback response when API is unavailable"""
        message_lower = message.lower()
        
        # Budget-related queries
        if any(word in message_lower for word in ['budget', 'spending', 'expenses']):
            total_expenses = user_context.get('total_expenses', 0)
            return f"""• Current spending: ₹{total_expenses:.2f}
• Use 50/30/20 rule (needs/wants/savings)
• Set category limits
• Review weekly

Set a budget in "Create Budget"!"""
        
        # Savings-related queries
        elif any(word in message_lower for word in ['save', 'saving', 'goal']):
            return """• Emergency fund: 3-6 months expenses
• Automate savings on payday
• Start with ₹500/month minimum
• Track progress weekly

Create goal in "Add Savings Goal"!"""
        
        # Expense tracking queries
        elif any(word in message_lower for word in ['track', 'transaction', 'expense']):
            category_spending = user_context.get('category_spending', {})
            if category_spending:
                top_category = max(category_spending, key=category_spending.get)
                return f"""• Top spending: {top_category} ₹{category_spending[top_category]:.2f}
• Log expenses immediately
• Review weekly
• Set category budgets

Use "Add Transaction"!"""
            else:
                return """• Start tracking all expenses
• Categorize each transaction
• Review patterns weekly
• Set monthly budgets

Click "Add Transaction"!"""
        
        # Investment queries
        elif any(word in message_lower for word in ['invest', 'investment', 'stocks', 'mutual fund']):
            return """• Build emergency fund first (3-6 months)
• Start with index funds/ETFs
• Use SIP for regular investing
• Diversify across sectors
• Learn before investing

Start small, stay consistent!"""
        
        # General greeting
        elif any(word in message_lower for word in ['hello', 'hi', 'hey', 'start']):
            return """Hi! I'm FinanceAI 👋

I help with:
• Track expenses
• Manage budgets
• Set savings goals
• Financial advice

Ask me anything!"""
        
        # Default response
        else:
            return """I can help with:
• Budgets & expenses
• Savings strategies
• Spending analysis
• Financial tips

What do you need?"""
    
    def predict_future_expenses(self, transactions: List[Dict]) -> Dict:
        """
        Predict future expenses based on historical data
        
        Args:
            transactions: List of transaction dictionaries
        
        Returns:
            Dictionary with predictions
        """
        if not transactions:
            return {
                'next_month_prediction': 0,
                'category_predictions': {},
                'trend': 'insufficient_data'
            }
        
        # Calculate average spending
        total_expense = sum(t['amount'] for t in transactions if t['transaction_type'] == 'expense')
        avg_monthly = total_expense / max(1, len(set(t['date'][:7] for t in transactions)))
        
        # Category-wise predictions
        category_totals = {}
        for t in transactions:
            if t['transaction_type'] == 'expense':
                category = t['category']
                category_totals[category] = category_totals.get(category, 0) + t['amount']
        
        # Determine trend
        if len(transactions) >= 2:
            recent = transactions[-len(transactions)//2:]
            older = transactions[:len(transactions)//2]
            recent_avg = sum(t['amount'] for t in recent if t['transaction_type'] == 'expense') / max(1, len(recent))
            older_avg = sum(t['amount'] for t in older if t['transaction_type'] == 'expense') / max(1, len(older))
            
            if recent_avg > older_avg * 1.1:
                trend = 'increasing'
            elif recent_avg < older_avg * 0.9:
                trend = 'decreasing'
            else:
                trend = 'stable'
        else:
            trend = 'stable'
        
        return {
            'next_month_prediction': round(avg_monthly * 1.05, 2),  # 5% buffer
            'category_predictions': {k: round(v / max(1, len(set(t['date'][:7] for t in transactions))), 2) 
                                    for k, v in category_totals.items()},
            'trend': trend,
            'confidence': 'medium' if len(transactions) > 10 else 'low'
        }
    
    def suggest_savings_goals(self, user_data: Dict) -> List[Dict]:
        """
        Suggest personalized savings goals
        
        Args:
            user_data: Dictionary with user's financial data
        
        Returns:
            List of suggested savings goals
        """
        suggestions = []
        
        total_income = user_data.get('total_income', 0)
        total_expenses = user_data.get('total_expenses', 0)
        surplus = total_income - total_expenses
        
        if surplus > 0:
            # Emergency fund
            suggestions.append({
                'name': 'Emergency Fund',
                'target_amount': total_expenses * 6,  # 6 months expenses
                'suggested_monthly': surplus * 0.3,
                'priority': 'high',
                'description': 'Build a safety net for unexpected expenses'
            })
            
            # Short-term savings
            suggestions.append({
                'name': 'Short-term Savings',
                'target_amount': total_income * 2,
                'suggested_monthly': surplus * 0.2,
                'priority': 'medium',
                'description': 'For upcoming purchases or experiences'
            })
            
            # Investment/Retirement
            suggestions.append({
                'name': 'Investment Fund',
                'target_amount': total_income * 12,
                'suggested_monthly': surplus * 0.3,
                'priority': 'medium',
                'description': 'Build wealth for the future'
            })
        
        return suggestions
    
    def analyze_spending_patterns(self, transactions: List[Dict]) -> Dict:
        """
        Analyze user's spending patterns
        
        Args:
            transactions: List of transaction dictionaries
        
        Returns:
            Dictionary with spending analysis
        """
        if not transactions:
            return {
                'total_expenses': 0,
                'top_categories': [],
                'insights': ['Start tracking expenses to get insights!']
            }
        
        # Calculate totals
        expense_transactions = [t for t in transactions if t['transaction_type'] == 'expense']
        total_expenses = sum(t['amount'] for t in expense_transactions)
        
        # Category analysis
        category_totals = {}
        for t in expense_transactions:
            category = t['category']
            category_totals[category] = category_totals.get(category, 0) + t['amount']
        
        # Sort by amount
        top_categories = sorted(category_totals.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Generate insights
        insights = []
        if top_categories:
            top_cat, top_amount = top_categories[0]
            percentage = (top_amount / total_expenses * 100) if total_expenses > 0 else 0
            insights.append(f"{top_cat} is your highest spending category at {percentage:.1f}% of total expenses")
        
        # Check for unusual patterns
        if category_totals.get('Shopping', 0) > total_expenses * 0.3:
            insights.append("Consider reducing shopping expenses - they're over 30% of your budget")
        
        if category_totals.get('Food & Dining', 0) > total_expenses * 0.25:
            insights.append("Dining expenses are high - cooking at home could save money")
        
        return {
            'total_expenses': round(total_expenses, 2),
            'top_categories': [{'category': cat, 'amount': amt, 'percentage': round(amt/total_expenses*100, 1)} 
                              for cat, amt in top_categories],
            'insights': insights if insights else ['Your spending looks balanced!']
        }
