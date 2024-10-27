import streamlit as st
import pandas as pd
from utils.database import get_db_connection
from components.charts import create_spending_pie_chart, create_spending_trend_line
from utils.ai_helper import analyze_spending_patterns

def load_dashboard_data(user_id):
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("""
            SELECT * FROM transactions 
            WHERE user_id = %s 
            ORDER BY date DESC
        """, (user_id,))
        transactions = cur.fetchall()
    return transactions

def dashboard():
    if 'user_id' not in st.session_state:
        st.warning("Please login to access the dashboard")
        st.stop()
    
    st.title("Financial Dashboard")
    
    transactions = load_dashboard_data(st.session_state['user_id'])
    if not transactions:
        st.info("No transactions found. Start by adding some expenses!")
        return
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(create_spending_pie_chart(transactions))
    
    with col2:
        st.plotly_chart(create_spending_trend_line(transactions))
    
    patterns = analyze_spending_patterns(transactions)
    
    st.subheader("Spending Insights")
    st.write("Top spending categories:", patterns['top_categories'])
    
    if patterns['unusual_transactions']:
        st.warning("Unusual transactions detected!")
        st.write(patterns['unusual_transactions'])

if __name__ == "__main__":
    dashboard()
