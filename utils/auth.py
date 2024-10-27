import streamlit as st
import bcrypt
import secrets
from utils.database import get_db_connection
from utils.email_helper import send_verification_email
from psycopg2 import errors

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))

def generate_verification_token() -> str:
    return secrets.token_urlsafe(32)

def verify_email_token(token: str) -> bool:
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("""
            UPDATE users 
            SET email_verified = TRUE, verification_token = NULL 
            WHERE verification_token = %s
            RETURNING id
        """, (token,))
        result = cur.fetchone()
        conn.commit()
    return result is not None

def login_user(email: str, password: str) -> bool:
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cur.fetchone()
        
    if user and verify_password(password, user[2]):
        if not user[7]:  # Check email_verified status
            st.error("Please verify your email before logging in. Check your inbox for the verification link.")
            return False
        st.session_state['user_id'] = user[0]
        st.session_state['subscription_type'] = user[3]
        return True
    return False

def register_user(email: str, password: str, subscription_type: str):
    conn = get_db_connection()
    password_hash = hash_password(password)
    verification_token = generate_verification_token()
    
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO users (
                    email, password_hash, subscription_type, subscription_status, 
                    created_at, email_verified, verification_token
                )
                VALUES (%s, %s, %s, 'active', NOW(), FALSE, %s)
                RETURNING id
            """, (email, password_hash, subscription_type, verification_token))
            user_id = cur.fetchone()[0]
            conn.commit()

        # Send verification email
        if send_verification_email(email, verification_token):
            st.info("Please check your email to verify your account.")
        else:
            st.warning("Could not send verification email. Please try again later.")
            
        return user_id
    except errors.UniqueViolation:
        st.error("An account with this email already exists. Please use a different email or login.")
        return None
    except Exception as e:
        st.error(f"Registration failed: {str(e)}")
        return None
