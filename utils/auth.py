import streamlit as st
import bcrypt
from utils.database import get_db_connection

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))

def login_user(email: str, password: str) -> bool:
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        
    if user and verify_password(password, user[2]):
        st.session_state['user_id'] = user[0]
        st.session_state['subscription_type'] = user[3]
        return True
    return False

def register_user(email: str, password: str, subscription_type: str):
    conn = get_db_connection()
    password_hash = hash_password(password)
    
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO users (email, password_hash, subscription_type, subscription_status, created_at)
            VALUES (%s, %s, %s, 'active', NOW())
            RETURNING id
        """, (email, password_hash, subscription_type))
        user_id = cur.fetchone()[0]
        conn.commit()
    
    return user_id
