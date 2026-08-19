"""Main Streamlit application with modular page structure."""

import streamlit as st
from config.styling import apply_custom_css, ICONS
from pages import dashboard, dataset, preprocessing, visualizations, prediction, model_comparison, history, about
from backend.user_service import authenticate_user
from database.init_db import init_db


# Initialize database
init_db()

# Apply custom styling
apply_custom_css()

# Initialize session state
def init_session_state():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
        st.session_state["user"] = None


init_session_state()

# Page configuration
st.set_page_config(
    page_title="Energy Consumption Prediction",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Sidebar navigation
def render_sidebar():
    """Render professional sidebar navigation."""
    with st.sidebar:
        # App title and branding
        st.markdown("""
            <div style='text-align: center; padding: 20px 0;'>
                <h1 style='font-size: 1.8em; color: #58a6ff;'>⚡ EnergyPred</h1>
                <p style='color: #8b949e; margin-top: -10px;'>Energy Management System</p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("---")

        if st.session_state.get("logged_in"):
            # User info card
            user_info = st.session_state['user']
            st.markdown(f"""
                <div style='background: rgba(31, 111, 235, 0.2); padding: 15px; border-radius: 8px; 
                            border-left: 4px solid #1f6feb;'>
                    <p style='margin: 0; color: #58a6ff; font-weight: bold;'>👤 Logged In</p>
                    <p style='margin: 5px 0 0 0; color: #e1e4e8;'>{user_info['username']}</p>
                    <p style='margin: 3px 0 0 0; color: #8b949e; font-size: 0.85em;'>{user_info['email']}</p>
                </div>
            """, unsafe_allow_html=True)

            st.markdown("---")

            st.markdown("### 📍 Navigation")

            # Main navigation menu with icons
            pages = {
                f"{ICONS.get('dashboard', '📊')} Dashboard": "dashboard",
                f"{ICONS.get('dataset', '📁')} Dataset": "dataset",
                f"{ICONS.get('preprocessing', '⚙️')} Preprocessing": "preprocessing",
                f"{ICONS.get('visualization', '📈')} Visualizations": "visualizations",
                f"{ICONS.get('predict', '⚡')} Predict Energy": "prediction",
                f"{ICONS.get('compare', '🏆')} Model Comparison": "model_comparison",
                f"{ICONS.get('history', '📜')} History": "history",
                f"{ICONS.get('about', 'ℹ️')} About": "about",
            }

            selected_page = st.radio(
                "Select a page:",
                list(pages.keys()),
                label_visibility="collapsed",
                key="page_selector"
            )

            st.markdown("---")

            # System info
            st.markdown("""
                <div style='background: rgba(36, 134, 54, 0.2); padding: 12px; border-radius: 8px;'>
                    <p style='margin: 0; color: #3fb950; font-size: 0.85em;'>🟢 System Status: Online</p>
                    <p style='margin: 3px 0 0 0; color: #8b949e; font-size: 0.75em;'>All services operational</p>
                </div>
            """, unsafe_allow_html=True)

            st.markdown("---")

            # Logout
            if st.button(f"{ICONS.get('logout', '🚪')} Logout", use_container_width=True):
                st.session_state["logged_in"] = False
                st.session_state["user"] = None
                st.rerun()

            return pages.get(selected_page)

        else:
            st.markdown("""
                <div style='background: rgba(218, 54, 51, 0.2); padding: 15px; border-radius: 8px; 
                            border-left: 4px solid #da3633; margin-top: 20px;'>
                    <p style='margin: 0; color: #f85149; font-weight: bold;'>🔒 Access Required</p>
                    <p style='margin: 5px 0 0 0; color: #e1e4e8; font-size: 0.9em;'>Please log in to access the dashboard</p>
                </div>
            """, unsafe_allow_html=True)
            return None


def render_login_page():
    """Render professional login and registration page."""
    # Professional header
    st.markdown(
        """
        <div style='text-align: center; padding: 40px 0;'>
            <h1 style='font-size: 3em; background: linear-gradient(135deg, #58a6ff 0%, #1f6feb 100%); 
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent;'>
                ⚡ Energy Consumption Prediction
            </h1>
            <p style='font-size: 1.2em; color: #79c0ff; margin-top: 10px;'>
                Advanced ML-Powered Energy Management System
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("---")

    col_left, col_spacer, col_right = st.columns([1, 0.1, 1])

    with col_left:
        st.markdown(
            """
            <div style='background: rgba(22, 27, 34, 0.7); padding: 30px; border-radius: 12px; 
                        border: 1px solid rgba(48, 54, 61, 0.8);'>
                <h2 style='color: #58a6ff; margin-bottom: 20px;'>🔓 Login</h2>
            </div>
            """,
            unsafe_allow_html=True
        )

        email_or_username = st.text_input(
            "Email or Username",
            placeholder="Enter your email or username",
            help="Your registered email or username"
        )
        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter your password",
            help="Your secure password"
        )

        col_login, col_forgot = st.columns(2)
        with col_login:
            if st.button("🔓 Login", key="login_btn", use_container_width=True):
                if not email_or_username or not password:
                    st.error("❌ Please enter both email/username and password")
                else:
                    user = authenticate_user(email_or_username, password)
                    if user:
                        st.session_state["logged_in"] = True
                        st.session_state["user"] = user
                        st.success(f"✅ Welcome back, {user['username']}!")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("❌ Invalid credentials. Please try again.")

        with col_forgot:
            st.button("🔑 Forgot Password?", disabled=True, use_container_width=True, help="Coming soon")

        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; color: #8b949e; font-size: 0.9em;'>
        <p>⚙️ Secure login with industry-standard encryption</p>
        </div>
        """, unsafe_allow_html=True)

    with col_right:
        st.markdown(
            """
            <div style='background: rgba(22, 27, 34, 0.7); padding: 30px; border-radius: 12px; 
                        border: 1px solid rgba(48, 54, 61, 0.8);'>
                <h2 style='color: #3fb950; margin-bottom: 20px;'>📋 Create Account</h2>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.write("New to Energy Prediction? Sign up now!")

        from backend.user_service import create_user
        from utils.security import validate_password

        username = st.text_input(
            "Username",
            placeholder="Choose a username",
            key="reg_username",
            help="3-20 characters"
        )
        email = st.text_input(
            "Email Address",
            placeholder="your@email.com",
            key="reg_email",
            help="We'll use this for account recovery"
        )
        password_new = st.text_input(
            "Password",
            type="password",
            placeholder="Create a strong password",
            key="register_password",
            help="Min 8 chars: uppercase, lowercase, digit, symbol"
        )
        confirm_password = st.text_input(
            "Confirm Password",
            type="password",
            placeholder="Re-enter your password",
            key="confirm_password"
        )

        if st.button("✍️ Create Account", key="register_btn", use_container_width=True):
            if not username or not email or not password_new or not confirm_password:
                st.error("❌ All fields are required")
            elif len(username) < 3:
                st.error("❌ Username must be at least 3 characters")
            elif password_new != confirm_password:
                st.error("❌ Passwords do not match")
            elif not validate_password(password_new):
                st.error("❌ Password must include: 8+ chars, uppercase, lowercase, digit, symbol")
            else:
                try:
                    created = create_user(username, email, password_new)
                    if created:
                        st.success("✅ Account created successfully! Please log in above.")
                        st.info("💡 Your account is ready to use. Log in with your credentials.")
                    else:
                        st.error("❌ Email already registered. Please use another email.")
                except Exception as e:
                    st.error(f"❌ Registration error: {str(e)}")

        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; color: #8b949e; font-size: 0.9em;'>
        <p>✓ Secure account creation</p>
        <p>✓ Privacy guaranteed</p>
        </div>
        """, unsafe_allow_html=True)


def render_page(page_name):
    if page_name == "dashboard":
        dashboard.render()
    elif page_name == "dataset":
        dataset.render()
    elif page_name == "preprocessing":
        preprocessing.render()
    elif page_name == "visualizations":
        visualizations.render()
    elif page_name == "prediction":
        prediction.render()
    elif page_name == "model_comparison":
        model_comparison.render()
    elif page_name == "history":
        history.render()
    elif page_name == "about":
        about.render()


def main():
    if not st.session_state.get("logged_in"):
        render_login_page()
    else:
        selected_page = render_sidebar()

        if selected_page:
            render_page(selected_page)

        # Logout button in sidebar
        with st.sidebar:
            st.markdown("---")
            if st.button(f"{ICONS['logout']} Logout", use_container_width=True):
                st.session_state["logged_in"] = False
                st.session_state["user"] = None
                st.rerun()


if __name__ == "__main__":
    main()
