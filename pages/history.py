"""Prediction history page module."""

import streamlit as st
import pandas as pd
from config.styling import ICONS
from backend.prediction_service import get_predictions_for_user, delete_prediction


def render():
    """Render the prediction history page."""
    st.set_page_config(page_title="Prediction History", page_icon="📋", layout="wide")

    st.title(f"{ICONS['history']} Prediction History")
    st.markdown("---")

    if "user" not in st.session_state or not st.session_state["user"]:
        st.warning("Please log in to view your prediction history.")
        return

    user_id = st.session_state["user"]["id"]

    # Get prediction history
    history = get_predictions_for_user(user_id)

    if len(history) == 0:
        st.info("No predictions yet. Go to Predict Energy to make your first prediction.")
        return

    # Create tabs
    tab1, tab2, tab3 = st.tabs(["View History", "Search", "Export"])

    with tab1:
        st.subheader("📊 Your Prediction History")
        df_history = pd.DataFrame(history)

        # Display as table
        st.dataframe(df_history, use_container_width=True)

        # Delete prediction
        st.subheader("🗑️ Delete Prediction")
        col1, col2 = st.columns(2)

        with col1:
            pred_id = st.number_input("Prediction ID to delete", min_value=1, step=1)

        with col2:
            if st.button("Delete"):
                success = delete_prediction(pred_id, user_id)
                if success:
                    st.success("✅ Prediction deleted!")
                    st.rerun()
                else:
                    st.error("Could not delete prediction.")

    with tab2:
        st.subheader("🔍 Search History")
        search_term = st.text_input("Search predictions:")

        if search_term:
            # Filter dataframe
            mask = df_history.astype(str).apply(lambda x: x.str.contains(search_term, case=False)).any(axis=1)
            filtered_df = df_history[mask]
            st.dataframe(filtered_df, use_container_width=True)

    with tab3:
        st.subheader("📥 Export History")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Download as CSV"):
                csv = df_history.to_csv(index=False)
                st.download_button(
                    label="Download CSV",
                    data=csv,
                    file_name="prediction_history.csv",
                    mime="text/csv",
                )

        with col2:
            st.info(f"Total predictions: {len(history)}")


if __name__ == "__main__":
    render()
