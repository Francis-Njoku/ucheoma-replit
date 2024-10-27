import streamlit as st
import bcrypt
import secrets
import logging
from utils.database import get_db_connection
from utils.email_helper import send_verification_email
from psycopg2 import errors

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password: str, password_hash: str) -> bool:
    return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))

def generate_verification_token() -> str:
    token = secrets.token_urlsafe(32)
    logger.info(f"Generated verification token: {token[:10]}... (truncated)")
    return token

def verify_email_token(token: str) -> bool:
    logger.info(f"Attempting to verify token: {token[:10]}... (truncated)")
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE users 
                SET email_verified = TRUE, verification_token = NULL 
                WHERE verification_token = %s
                RETURNING id
            """, (token,))
            result = cur.fetchone()
            conn.commit()
            
            if result:
                logger.info("Email verification successful!")
            else:
                logger.warning("Invalid or expired verification token")
                
            return result is not None
    except Exception as e:
        logger.error(f"Error verifying email token: {str(e)}")
        return False
    finally:
        conn.close()

def login_user(email: str, password: str) -> bool:
    logger.info(f"Attempting login for user: {email}")
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cur.fetchone()
            
        if not user:
            logger.warning(f"No user found with email: {email}")
            return False
            
        if verify_password(password, user[2]):
            if not user[7]:  # Check email_verified status
                logger.warning(f"Unverified email attempt to login: {email}")
                st.error("Please verify your email before logging in. Check your inbox for the verification link.")
                return False
            logger.info(f"Successful login for user: {email}")
            st.session_state['user_id'] = user[0]
            st.session_state['subscription_type'] = user[3]
            return True
        else:
            logger.warning(f"Invalid password attempt for user: {email}")
            return False
    finally:
        conn.close()

def register_user(email: str, password: str, subscription_type: str):
    logger.info(f"Starting registration process for: {email}")
    conn = get_db_connection()
    
    try:
        password_hash = hash_password(password)
        verification_token = generate_verification_token()
        
        logger.info("Inserting new user into database...")
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
            
        logger.info(f"User created successfully with ID: {user_id}")

        # Send verification email
        logger.info("Attempting to send verification email...")
        email_result = send_verification_email(email, verification_token)
        
        if email_result is True:
            logger.info("Verification email sent successfully")
            st.info("Please check your email to verify your account.")
        else:
            logger.error("Failed to send verification email")
            st.warning("""
                Account created but verification email could not be sent.
                Please contact support for assistance with email verification.
            """)
            
        return user_id
        
    except errors.UniqueViolation:
        logger.error(f"Registration failed: Email already exists: {email}")
        st.error("An account with this email already exists. Please use a different email or login.")
        return None
    except Exception as e:
        logger.error(f"Registration failed with unexpected error: {str(e)}")
        st.error(f"Registration failed due to an unexpected error. Please try again later.")
        return None
    finally:
        conn.close()
