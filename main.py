import streamlit as st
from utils.database import init_db
from utils.auth import login_user, register_user
from utils.stripe_helper import create_checkout_session

st.set_page_config(
    page_title="AI Financial Assistant",
    page_icon="💰",
    layout="wide"
)

def main():
    init_db()
    
    if 'user_id' not in st.session_state:
        st.title("Welcome to AI Financial Assistant")
        
        tab1, tab2 = st.tabs(["Login", "Register"])
        
        with tab1:
            with st.form("login_form"):
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                submit = st.form_submit_button("Login")
                
                if submit:
                    if login_user(email, password):
                        st.success("Login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid credentials")
        
        with tab2:
            with st.form("register_form"):
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                subscription = st.selectbox(
                    "Subscription Type",
                    options=['basic', 'premium'],
                    format_func=lambda x: f"{x.title()} (${25 if x == 'premium' else 10}/month)"
                )
                submit = st.form_submit_button("Register")
                
                if submit:
                    user_id = register_user(email, password, subscription)
                    if user_id:
                        checkout_url = create_checkout_session(user_id, subscription)
                        if checkout_url:
                            st.success("Registration successful! Redirecting to payment...")
                            st.markdown(f'<meta http-equiv="refresh" content="2;url={checkout_url}">', unsafe_allow_html=True)
                        else:
                            st.error("Error creating payment session")
    else:
        st.sidebar.success("Logged in successfully!")
        if st.sidebar.button("Logout"):
            st.session_state.clear()
            st.rerun()

if __name__ == "__main__":
    main()
