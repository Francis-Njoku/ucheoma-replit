import os
import requests
import logging
from typing import Optional, Dict, Union

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

MAILGUN_API_KEY = os.environ.get('MAILGUN_API_KEY')
MAILGUN_DOMAIN = os.environ.get('MAILGUN_DOMAIN', 'sandbox.mailgun.org')  # Get from environment or use sandbox
FROM_EMAIL = f"AI Financial Assistant <mailgun@{MAILGUN_DOMAIN}>"

def send_verification_email(to_email: str, verification_token: str) -> Union[bool, Dict]:
    """
    Send a verification email using Mailgun.
    Returns True if successful, False if failed, or response dict for debugging.
    """
    if not MAILGUN_API_KEY:
        logger.error("Mailgun API key is missing! Please set MAILGUN_API_KEY environment variable.")
        return False

    logger.info(f"Attempting to send verification email to: {to_email}")
    logger.info(f"Using Mailgun domain: {MAILGUN_DOMAIN}")
    
    try:
        verification_url = f"http://0.0.0.0:5000/verify_email?token={verification_token}"
        
        email_data = {
            "from": FROM_EMAIL,
            "to": to_email,
            "subject": "Verify your email address",
            "text": f"""
            Welcome to AI Financial Assistant!
            
            Please verify your email address by clicking the link below:
            
            {verification_url}
            
            If you didn't create this account, please ignore this email.
            """,
            "html": f"""
            <h2>Welcome to AI Financial Assistant!</h2>
            <p>Please verify your email address by clicking the link below:</p>
            <p><a href="{verification_url}">Verify Email Address</a></p>
            <p>If you didn't create this account, please ignore this email.</p>
            """
        }

        logger.info("Sending verification email...")
        response = requests.post(
            f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
            auth=("api", MAILGUN_API_KEY),
            data=email_data
        )
        
        # Log the full response for debugging
        logger.info(f"Mailgun API Response: {response.text}")
        
        if response.status_code == 200:
            logger.info("Email sent successfully!")
            return True
        else:
            logger.error(f"Failed to send email. Status code: {response.status_code}")
            logger.error(f"Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        logger.error(f"Network error while sending email: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error while sending email: {str(e)}")
        return False
