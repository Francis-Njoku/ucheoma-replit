import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

def create_spending_pie_chart(transactions):
    df = pd.DataFrame(transactions)
    fig = px.pie(df, values='amount', names='category', title='Spending by Category')
    return fig

def create_spending_trend_line(transactions):
    df = pd.DataFrame(transactions)
    df['date'] = pd.to_datetime(df['date'])
    daily_spending = df.groupby('date')['amount'].sum().reset_index()
    
    fig = px.line(daily_spending, x='date', y='amount', 
                  title='Daily Spending Trend')
    return fig

def create_budget_progress_bars(budget, actual):
    categories = list(budget.keys())
    
    fig = go.Figure()
    for category in categories:
        fig.add_trace(go.Bar(
            name=category,
            x=[actual[category] / budget[category] * 100],
            y=[category],
            orientation='h'
        ))
    
    fig.update_layout(title='Budget Progress')
    return fig
