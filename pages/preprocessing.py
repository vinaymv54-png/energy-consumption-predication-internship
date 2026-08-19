"""Data preprocessing page module."""

import streamlit as st
from config.styling import ICONS
from utils.data_processor import DataProcessor, FeatureEngineer


def render():
    """Render the preprocessing page."""
    st.set_page_config(page_title="Data Preprocessing", page_icon="🧹", layout="wide")

    st.title(f"{ICONS['preprocessing']} Data Preprocessing")
    st.markdown("---")

    if "uploaded_df" not in st.session_state:
        st.warning("Please upload a dataset first from the Dataset section.")
        return

    df = st.session_state["uploaded_df"]
    original_shape = df.shape

    # Create tabs for preprocessing operations
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Handle Missing Values",
        "Remove Duplicates",
        "Remove Outliers",
        "Feature Engineering",
        "Summary"
    ])

    # Tab 1: Handle Missing Values
    with tab1:
        st.subheader("Handle Missing Values")

        col1, col2 = st.columns(2)

        with col1:
            missing_info = DataProcessor.get_missing_values_report(df)
            if len(missing_info) > 0:
                st.dataframe(missing_info, use_container_width=True)
            else:
                st.success("✅ No missing values found!")

        with col2:
            strategy = st.radio("Select strategy:", ["mean", "median", "drop"])

            if st.button("🔧 Apply Missing Value Handling"):
                df_cleaned = DataProcessor.handle_missing_values(df, strategy=strategy)
                st.session_state["uploaded_df"] = df_cleaned
                st.success(f"✅ Applied {strategy} strategy!")
                st.dataframe(df_cleaned.head(), use_container_width=True)

    # Tab 2: Remove Duplicates
    with tab2:
        st.subheader("Remove Duplicate Records")

        col1, col2 = st.columns(2)

        with col1:
            st.info(f"Total records: {len(df)}")
            duplicate_count = df.duplicated().sum()
            st.metric("Duplicate Records", duplicate_count)

        with col2:
            if st.button("🔧 Remove Duplicates"):
                df_no_dup, removed = DataProcessor.remove_duplicates(df)
                st.session_state["uploaded_df"] = df_no_dup
                st.success(f"✅ Removed {removed} duplicate records!")
                st.metric("Remaining Records", len(df_no_dup))

    # Tab 3: Remove Outliers
    with tab3:
        st.subheader("Remove Outliers")

        numeric_cols = df.select_dtypes(include=["float64", "int64"]).columns.tolist()

        if numeric_cols:
            col1, col2 = st.columns(2)

            with col1:
                selected_col = st.selectbox("Select column for outlier detection", numeric_cols)

            with col2:
                method = st.radio("Select method:", ["iqr", "zscore"])

            if st.button("🔧 Remove Outliers"):
                df_no_outliers = DataProcessor.remove_outliers(df, selected_col, method=method)
                removed_count = len(df) - len(df_no_outliers)
                st.session_state["uploaded_df"] = df_no_outliers
                st.success(f"✅ Removed {removed_count} outliers using {method}!")
        else:
            st.info("No numeric columns found in dataset.")

    # Tab 4: Feature Engineering
    with tab4:
        st.subheader("Feature Engineering")

        col1, col2 = st.columns(2)

        with col1:
            if "Datetime" in df.columns or "Date" in df.columns:
                if st.button("📅 Create Temporal Features"):
                    datetime_col = "Datetime" if "Datetime" in df.columns else "Date"
                    df_features = FeatureEngineer.create_temporal_features(df, datetime_col)
                    st.session_state["uploaded_df"] = df_features
                    st.success("✅ Temporal features created!")
                    new_cols = [col for col in df_features.columns if col not in df.columns]
                    st.info(f"New features: {', '.join(new_cols)}")

        with col2:
            if st.button("🔤 Encode Categorical Variables"):
                df_encoded = FeatureEngineer.encode_categorical_features(df)
                st.session_state["uploaded_df"] = df_encoded
                st.success("✅ Categorical variables encoded!")

        # Show preprocessing summary
        st.subheader("Preprocessing Options")
        col1, col2, col3 = st.columns(3)

        with col1:
            if st.button("📊 Normalize Features"):
                df_normalized = FeatureEngineer.normalize_numeric_features(df)
                st.session_state["uploaded_df"] = df_normalized
                st.success("✅ Features normalized!")

        with col2:
            st.info("Use the buttons to apply transformations")

        with col3:
            st.info("Order matters - handle missing values first!")

    # Tab 5: Summary
    with tab5:
        st.subheader("📋 Preprocessing Summary")

        current_shape = st.session_state["uploaded_df"].shape

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Original Rows", original_shape[0])
            st.metric("Current Rows", current_shape[0])

        with col2:
            st.metric("Original Columns", original_shape[1])
            st.metric("Current Columns", current_shape[1])

        with col3:
            st.metric("Rows Removed", original_shape[0] - current_shape[0])
            st.metric("Features Added", current_shape[1] - original_shape[1])

        with col4:
            info = DataProcessor.get_dataset_info(st.session_state["uploaded_df"])
            st.metric("Total Missing Values", info["Missing Values"])
            st.metric("Duplicate Records", info["Duplicate Rows"])

        st.success("✅ Preprocessing complete! You can now train the model.")


if __name__ == "__main__":
    render()
