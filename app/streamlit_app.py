import streamlit as st
import pandas as pd
from pathlib import Path
from backend.user_service import create_user, authenticate_user
from backend.prediction_service import save_prediction, get_predictions_for_user, delete_prediction
from backend.admin_service import get_totals
from utils.model_utils import predict_energy
from utils.security import validate_password


def init_session_state():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
        st.session_state["user"] = None
        st.session_state["prediction_result"] = None


def login_page():
    st.title("Login")

    email_or_username = st.text_input("Email or Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if not email_or_username or not password:
            st.error("Please enter email/username and password")
            return

        user = authenticate_user(email_or_username, password)
        if user:
            st.session_state["logged_in"] = True
            st.session_state["user"] = user
            st.success(f"Welcome back, {user['username']}!")
            st.rerun()
        else:
            st.error("Invalid email or password")


def register_page():
    st.title("Register")
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    confirm_password = st.text_input("Confirm password", type="password")

    if st.button("Register"):
        if not username or not email or not password or not confirm_password:
            st.error("All fields are required")
            return
        if password != confirm_password:
            st.error("Passwords do not match")
            return
        if not validate_password(password):
            st.error("Password must be at least 8 characters and include uppercase, lowercase, digit, and symbol.")
            return

        created = create_user(username, email, password)
        if created:
            st.success("Registration complete. Please log in.")
        else:
            st.error("Email already registered.")


def dashboard_page():
    st.title("Dashboard")
    st.write("Monitor users, predictions, and model performance.")

    totals = get_totals()
    st.metric("Total registered users", totals["total_users"])
    st.metric("Total saved predictions", totals["total_predictions"])

    st.write("Use the sidebar to navigate to prediction, analytics, history, profile, or about pages.")


def prediction_page():
    st.title("Energy Prediction")
    st.write("Enter the feature values to generate an hourly energy consumption prediction.")

    hour = st.number_input("Hour of day", min_value=0, max_value=23, value=12)
    day_of_week = st.number_input("Day of week", min_value=0, max_value=6, value=2)
    month = st.number_input("Month", min_value=1, max_value=12, value=6)
    is_weekend = st.selectbox("Is weekend", [0, 1])
    lag_1 = st.number_input("Lag 1 (previous hour)", value=14000.0)
    lag_24 = st.number_input("Lag 24 (same hour previous day)", value=15000.0)
    rolling_6 = st.number_input("Rolling 6-hour average", value=14500.0)
    rolling_24 = st.number_input("Rolling 24-hour average", value=14800.0)

    if st.button("Predict"):
        input_values = {
            "hour": int(hour),
            "day_of_week": int(day_of_week),
            "month": int(month),
            "is_weekend": int(is_weekend),
            "lag_1": float(lag_1),
            "lag_24": float(lag_24),
            "rolling_6": float(rolling_6),
            "rolling_24": float(rolling_24),
        }
        prediction = predict_energy(input_values)
        save_prediction(st.session_state["user"]["id"], input_values, prediction)
        st.success(f"Predicted energy consumption: {prediction:.2f} MW")


def analytics_page():
    st.title("Analytics")
    st.write("View evaluation charts and dataset summaries.")

    chart_path = Path(__file__).resolve().parent.parent / "data" / "processed" / "evaluation_actual_vs_predicted.csv"
    if chart_path.exists():
        df_chart = pd.read_csv(chart_path)
        if "actual" in df_chart.columns and "predicted" in df_chart.columns:
            st.subheader("Actual vs Predicted")
            st.line_chart(df_chart.rename(columns={"actual": "Actual", "predicted": "Predicted"})[["Actual", "Predicted"]])
        else:
            st.error("Evaluation CSV does not contain required columns.")
    else:
        st.error("Evaluation CSV not found. Run evaluation before using analytics.")


def history_page():
    st.title("Prediction History")
    history = get_predictions_for_user(st.session_state["user"]["id"])
    if len(history) == 0:
        st.info("No prediction history available.")
        return

    df_history = pd.DataFrame(history)
    st.dataframe(df_history)

    prediction_id = st.number_input("Prediction ID to delete", min_value=1, step=1)
    if st.button("Delete prediction"):
        deleted = delete_prediction(prediction_id, st.session_state["user"]["id"])
        if deleted:
            st.success("Prediction deleted successfully.")
        else:
            st.error("Prediction could not be deleted.")


def profile_page():
    st.title("Profile")
    user = st.session_state["user"]
    st.write(f"Username: {user['username']}")
    st.write(f"Email: {user['email']}")
    st.write(f"User ID: {user['id']}")


def about_page():
    st.title("About")
    st.write("Energy Consumption Prediction application built with Streamlit and SQLite.")
    st.write("This app uses the existing trained Random Forest model and keeps prediction history per user.")


def main():
    init_session_state()

    if st.session_state["logged_in"]:
        page = st.sidebar.selectbox(
            "Navigation",
            ["Dashboard", "Prediction", "Analytics", "Prediction History", "Profile", "About", "Logout"],
        )
        if page == "Dashboard":
            dashboard_page()
        elif page == "Prediction":
            prediction_page()
        elif page == "Analytics":
            analytics_page()
        elif page == "Prediction History":
            history_page()
        elif page == "Profile":
            profile_page()
        elif page == "About":
            about_page()
        elif page == "Logout":
            st.session_state["logged_in"] = False
            st.session_state["user"] = None
            st.success("Logged out successfully.")
    else:
        page = st.sidebar.selectbox("Authentication", ["Login", "Register"])
        if page == "Login":
            login_page()
        else:
            register_page()


if __name__ == "__main__":
    main()
