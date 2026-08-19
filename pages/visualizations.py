"""Data visualization page module."""

import streamlit as st
import pandas as pd
from config.styling import ICONS
from utils.visualizations import (
    create_energy_trend_chart, create_scatter_chart, create_correlation_heatmap,
    create_distribution_chart, create_hourly_consumption_chart
)


def render():
    """Render the visualization page."""
    st.set_page_config(page_title="Visualizations", page_icon="📈", layout="wide")

    st.title(f"{ICONS['visualization']} Data Visualizations")
    st.markdown("---")

    # Load data
    try:
        df = pd.read_csv("data/processed/AEP_hourly_clean.csv", parse_dates=["Datetime"])
    except FileNotFoundError:
        st.warning("Could not load processed data. Please run preprocessing first.")
        return

    # Create tabs for different visualizations
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Energy Trend",
        "Correlations",
        "Distributions",
        "Comparisons",
        "Custom"
    ])

    with tab1:
        st.subheader("Energy Consumption Trend")
        chart = create_energy_trend_chart(df)
        if chart:
            st.plotly_chart(chart, use_container_width=True)

    with tab2:
        st.subheader("Correlation Heatmap")
        chart = create_correlation_heatmap(df)
        if chart:
            st.plotly_chart(chart, use_container_width=True)

    with tab3:
        st.subheader("Distribution Analysis")
        numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns
        selected_col = st.selectbox("Select column for distribution", numeric_cols)

        chart = create_distribution_chart(df, selected_col)
        if chart:
            st.plotly_chart(chart, use_container_width=True)

    with tab4:
        st.subheader("Hourly Consumption Analysis")
        if "hour" in df.columns and "AEP_MW" in df.columns:
            chart = create_hourly_consumption_chart(df)
            if chart:
                st.plotly_chart(chart, use_container_width=True)

    with tab5:
        st.subheader("Create Custom Chart")

        col1, col2 = st.columns(2)
        numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns

        with col1:
            x_col = st.selectbox("Select X-axis column", numeric_cols)

        with col2:
            y_col = st.selectbox("Select Y-axis column", numeric_cols, index=min(1, len(numeric_cols)-1))

        chart = create_scatter_chart(df, x_col, y_col)
        if chart:
            st.plotly_chart(chart, use_container_width=True)


if __name__ == "__main__":
    render()
