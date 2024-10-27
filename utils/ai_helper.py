import pandas as pd
import numpy as np
from typing import List, Dict

def analyze_spending_patterns(transactions: List[Dict]) -> Dict:
    df = pd.DataFrame(transactions)
    
    patterns = {
        'top_categories': df.groupby('category')['amount'].sum().nlargest(5).to_dict(),
        'monthly_trend': df.groupby(pd.Grouper(key='date', freq='M'))['amount'].sum().to_dict(),
        'unusual_transactions': df[df['amount'] > df['amount'].quantile(0.95)].to_dict('records')
    }
    
    return patterns

def generate_budget_recommendations(income: float, expenses: List[Dict]) -> Dict:
    total_expenses = sum(expense['amount'] for expense in expenses)
    
    recommendations = {
        'savings_target': income * 0.2,
        'expense_limits': {
            'housing': income * 0.3,
            'transportation': income * 0.15,
            'food': income * 0.15,
            'utilities': income * 0.1,
            'entertainment': income * 0.1,
            'others': income * 0.2
        },
        'alert_categories': []
    }
    
    return recommendations
