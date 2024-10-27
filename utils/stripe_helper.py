import stripe
import streamlit as st

stripe.api_key = st.secrets["STRIPE_SECRET_KEY"]

PRICE_IDS = {
    'basic': 'price_basic',  # Replace with actual Stripe price IDs
    'premium': 'price_premium'
}

def create_checkout_session(user_id: int, subscription_type: str):
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price': PRICE_IDS[subscription_type],
                'quantity': 1,
            }],
            mode='subscription',
            success_url='http://localhost:5000/success',
            cancel_url='http://localhost:5000/cancel',
            client_reference_id=str(user_id)
        )
        return checkout_session.url
    except Exception as e:
        st.error(f"Error creating checkout session: {str(e)}")
        return None
