"""Energy prediction page module."""

import streamlit as st
import joblib
from pathlib import Path
from config.styling import ICONS
from utils.recommendations import RecommendationEngine


def render():
    """Render the prediction page."""
    st.set_page_config(page_title="Predict Energy", page_icon="🔮", layout="wide")

    st.title(f"{ICONS['predict']} Energy Consumption Prediction")
    st.markdown("---")

    # Load trained model
    model_path = Path("models/random_forest_aep.joblib")
    scaler_path = Path("models/feature_scaler.joblib")

    if not model_path.exists() or not scaler_path.exists():
        st.error("Model files not found. Please train the model first.")
        return

    model = joblib.load(model_path)
    scaler = joblib.load(scaler_path)

    # Create two columns
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📊 Enter Feature Values")

        # Input fields
        hour = st.slider("Hour of Day", 0, 23, 12)
        day_of_week = st.slider("Day of Week (0-6)", 0, 6, 2)
        month = st.slider("Month", 1, 12, 6)
        is_weekend = st.selectbox("Is Weekend?", [0, 1], format_func=lambda x: "Yes" if x == 1 else "No")

        st.subheader("⚡ Energy Features")
        lag_1 = st.number_input("Lag 1 (Previous Hour)", value=14000.0, step=100.0)
        lag_24 = st.number_input("Lag 24 (Previous Day Same Hour)", value=15000.0, step=100.0)
        rolling_6 = st.number_input("Rolling 6-Hour Average", value=14500.0, step=100.0)
        rolling_24 = st.number_input("Rolling 24-Hour Average", value=14800.0, step=100.0)

    with col2:
        st.subheader("🔮 Prediction Result")

        if st.button("🚀 Predict Energy Consumption", key="predict_btn"):
            # Prepare input features
            features = [[hour, day_of_week, month, is_weekend, lag_1, lag_24, rolling_6, rolling_24]]

            # Scale features
            features_scaled = scaler.transform(features)

            # Make prediction
            prediction = model.predict(features_scaled)[0]

            # Store prediction
            st.session_state["last_prediction"] = prediction
            st.session_state["last_features"] = {
                "hour": hour,
                "day_of_week": day_of_week,
                "month": month,
                "is_weekend": is_weekend,
            }

        if "last_prediction" in st.session_state:
            prediction = st.session_state["last_prediction"]

            # Display prediction with color coding
            st.metric("⚡ Predicted Energy Consumption", f"{prediction:.2f} MW")

            # Consumption level indicator
            if prediction < 10:
                st.success(f"🟢 Low Consumption - {RecommendationEngine.get_consumption_level_text(prediction)}")
            elif prediction < 20:
                st.warning(f"🟡 Moderate Consumption - {RecommendationEngine.get_consumption_level_text(prediction)}")
            else:
                st.error(f"🔴 High Consumption - {RecommendationEngine.get_consumption_level_text(prediction)}")

            # Get recommendations
            recommendations = RecommendationEngine.get_recommendations(
                energy_consumption=prediction,
                temperature=25.5,
                humidity=65,
            )

            st.subheader("💡 Energy Saving Recommendations")
            for rec in recommendations["recommendations"]:
                st.info(rec)

            # Save to history
            if st.button("💾 Save Prediction"):
                from backend.prediction_service import save_prediction
                if "user" in st.session_state and st.session_state["user"]:
                    input_values = st.session_state.get("last_features", {})
                    save_prediction(st.session_state["user"]["id"], input_values, prediction)
                    st.success("✅ Prediction saved to history!")
                else:
                    st.warning("Please log in to save predictions.")


if __name__ == "__main__":
    render()
