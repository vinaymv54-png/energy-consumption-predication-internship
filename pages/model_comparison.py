"""Model comparison page module."""

import streamlit as st
import pandas as pd
from config.styling import ICONS


def render():
    """Render the model comparison page."""
    st.set_page_config(page_title="Model Comparison", page_icon="🏆", layout="wide")

    st.title(f"{ICONS['compare']} Model Comparison")
    st.markdown("---")

    st.info("📊 Compare performance of different ML models")

    # Mock model metrics
    mock_metrics = {
        "Linear Regression": {"R2": 0.5234, "MAE": 3.45, "MSE": 15.67, "RMSE": 3.96},
        "Decision Tree": {"R2": 0.6120, "MAE": 2.89, "MSE": 12.34, "RMSE": 3.51},
        "Random Forest": {"R2": 0.7856, "MAE": 2.35, "MSE": 7.89, "RMSE": 2.81},
        "XGBoost": {"R2": 0.7621, "MAE": 2.56, "MSE": 8.76, "RMSE": 2.96},
    }

    # Display metrics as DataFrame
    df_metrics = pd.DataFrame(mock_metrics).T
    df_metrics = df_metrics.round(4)

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("📊 Model Performance Metrics")
        st.dataframe(df_metrics, use_container_width=True)

    with col2:
        st.subheader("🏆 Best Model")
        best_model = df_metrics["R2"].idxmax()
        best_r2 = df_metrics.loc[best_model, "R2"]
        st.success(f"**{best_model}**")
        st.metric("R² Score", f"{best_r2:.4f}")

    st.markdown("---")

    # Comparison charts
    tab1, tab2, tab3 = st.tabs(["R² Scores", "Error Metrics", "All Metrics"])

    with tab1:
        st.bar_chart(df_metrics["R2"].sort_values(ascending=False))

    with tab2:
        st.bar_chart(df_metrics[["MAE", "RMSE"]].sort_values("MAE", ascending=False))

    with tab3:
        st.subheader("Detailed Comparison")
        st.dataframe(df_metrics, use_container_width=True)

        # Download comparison report
        if st.button("📥 Download Comparison Report"):
            csv = df_metrics.to_csv()
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name="model_comparison.csv",
                mime="text/csv",
            )


if __name__ == "__main__":
    render()
