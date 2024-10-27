import os
import requests
from typing import Optional

MAILGUN_API_KEY = os.environ.get('MAILGUN_API_KEY')
MAILGUN_DOMAIN = "sandbox.mailgun.org"  # Replace with your domain
FROM_EMAIL = f"AI Financial Assistant <mailgun@{MAILGUN_DOMAIN}>"

def send_verification_email(to_email: str, verification_token: str) -> Optional[bool]:
    """Send a verification email using Mailgun."""
    try:
        verification_url = f"http://0.0.0.0:5000/verify_email?token={verification_token}"
        
        response = requests.post(
            f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
            auth=("api", MAILGUN_API_KEY),
            data={
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
        )
        return response.status_code == 200
    except Exception as e:
        print(f"Error sending verification email: {str(e)}")
        return None
