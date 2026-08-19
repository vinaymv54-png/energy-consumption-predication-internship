"""Dataset management page module."""

import streamlit as st
import pandas as pd
import io
from config.styling import ICONS
from utils.data_processor import DataProcessor


def render():
    """Render the dataset page."""
    st.set_page_config(page_title="Dataset", page_icon="📂", layout="wide")

    st.title(f"{ICONS['dataset']} Dataset Management")
    st.markdown("---")

    # Tabs for different dataset operations
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
        "Upload Dataset",
        "View Dataset",
        "Dataset Preview",
        "Dataset Info",
        "Search Dataset",
        "Download Dataset"
    ])

    # Tab 1: Upload Dataset
    with tab1:
        st.subheader("📤 Upload CSV Dataset")
        uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.success(f"✅ File uploaded successfully! Shape: {df.shape}")
            st.session_state["uploaded_df"] = df

            # Show first few rows
            st.subheader("Preview of Uploaded Data")
            st.dataframe(df.head(10), use_container_width=True)

    # Tab 2: View Dataset
    with tab2:
        st.subheader("👁️ View Full Dataset")

        if "uploaded_df" in st.session_state:
            df = st.session_state["uploaded_df"]
            st.dataframe(df, use_container_width=True)
        else:
            st.info("Please upload a dataset first.")

    # Tab 3: Dataset Preview
    with tab3:
        st.subheader("📋 Dataset Preview")

        if "uploaded_df" in st.session_state:
            df = st.session_state["uploaded_df"]
            rows = st.slider("Number of rows to preview", 1, len(df), min(10, len(df)))
            st.dataframe(df.head(rows), use_container_width=True)
        else:
            st.info("Please upload a dataset first.")

    # Tab 4: Dataset Info
    with tab4:
        st.subheader("ℹ️ Dataset Information")

        if "uploaded_df" in st.session_state:
            df = st.session_state["uploaded_df"]
            info = DataProcessor.get_dataset_info(df)

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Rows", info["Total Rows"])
                st.metric("Numeric Columns", info["Numeric Columns"])
                st.metric("Missing Values", info["Missing Values"])

            with col2:
                st.metric("Total Columns", info["Total Columns"])
                st.metric("Categorical Columns", info["Categorical Columns"])
                st.metric("Duplicate Rows", info["Duplicate Rows"])

            with col3:
                st.metric("Memory Usage (MB)", f"{info['Memory Usage (MB)']:.2f}")

            # Data types report
            st.subheader("Data Types Report")
            dtype_report = DataProcessor.get_data_types_report(df)
            st.dataframe(dtype_report, use_container_width=True)

            # Missing values report
            if info["Missing Values"] > 0:
                st.subheader("Missing Values Report")
                missing_report = DataProcessor.get_missing_values_report(df)
                st.dataframe(missing_report, use_container_width=True)
        else:
            st.info("Please upload a dataset first.")

    # Tab 5: Search Dataset
    with tab5:
        st.subheader("🔍 Search Dataset")

        if "uploaded_df" in st.session_state:
            df = st.session_state["uploaded_df"]

            # Get column names
            columns = df.columns.tolist()
            search_column = st.selectbox("Select column to search", columns)
            search_value = st.text_input("Enter value to search")

            if search_value:
                filtered_df = df[df[search_column].astype(str).str.contains(search_value, case=False, na=False)]
                st.success(f"Found {len(filtered_df)} matching records")
                st.dataframe(filtered_df, use_container_width=True)
        else:
            st.info("Please upload a dataset first.")

    # Tab 6: Download Dataset
    with tab6:
        st.subheader("📥 Download Dataset")

        if "uploaded_df" in st.session_state:
            df = st.session_state["uploaded_df"]

            col1, col2 = st.columns(2)

            with col1:
                if st.button("📥 Download as CSV"):
                    csv_buffer = io.StringIO()
                    df.to_csv(csv_buffer, index=False)
                    st.download_button(
                        label="Download CSV",
                        data=csv_buffer.getvalue(),
                        file_name="dataset.csv",
                        mime="text/csv",
                    )

            with col2:
                if st.button("📥 Download as Excel"):
                    excel_buffer = io.BytesIO()
                    df.to_excel(excel_buffer, index=False)
                    st.download_button(
                        label="Download Excel",
                        data=excel_buffer.getvalue(),
                        file_name="dataset.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    )
        else:
            st.info("Please upload a dataset first.")


if __name__ == "__main__":
    render()
