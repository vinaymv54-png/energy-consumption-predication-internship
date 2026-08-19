"""Data processing and analysis utilities."""

import pandas as pd
import numpy as np


class DataProcessor:
    """Data processing and cleaning utilities."""

    @staticmethod
    def handle_missing_values(df, strategy="mean"):
        """Handle missing values in dataset."""
        df = df.copy()
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        categorical_cols = df.select_dtypes(include=["object"]).columns

        if strategy == "mean":
            df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
        elif strategy == "median":
            df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
        elif strategy == "drop":
            df = df.dropna()

        df[categorical_cols] = df[categorical_cols].fillna("Unknown")
        return df

    @staticmethod
    def remove_duplicates(df):
        """Remove duplicate records."""
        initial_count = len(df)
        df = df.drop_duplicates().reset_index(drop=True)
        removed_count = initial_count - len(df)
        return df, removed_count

    @staticmethod
    def remove_outliers(df, col, method="iqr"):
        """Remove outliers using IQR or Z-score method."""
        df = df.copy()
        if method == "iqr":
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
        elif method == "zscore":
            z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
            df = df[z_scores < 3]
        return df

    @staticmethod
    def get_dataset_info(df):
        """Get detailed dataset information."""
        info = {
            "Total Rows": len(df),
            "Total Columns": len(df.columns),
            "Numeric Columns": len(df.select_dtypes(include=[np.number]).columns),
            "Categorical Columns": len(df.select_dtypes(include=["object"]).columns),
            "Missing Values": df.isnull().sum().sum(),
            "Duplicate Rows": df.duplicated().sum(),
            "Memory Usage (MB)": df.memory_usage(deep=True).sum() / 1024 ** 2,
        }
        return info

    @staticmethod
    def get_missing_values_report(df):
        """Get missing values report."""
        missing = pd.DataFrame({
            "Column": df.columns,
            "Missing Count": df.isnull().sum().values,
            "Missing Percentage": (df.isnull().sum().values / len(df) * 100).round(2),
        })
        return missing[missing["Missing Count"] > 0].sort_values("Missing Count", ascending=False)

    @staticmethod
    def get_data_types_report(df):
        """Get data types report."""
        return pd.DataFrame({
            "Column": df.columns,
            "Data Type": df.dtypes.values,
            "Unique Values": df.nunique().values,
        })


class FeatureEngineer:
    """Feature engineering utilities."""

    @staticmethod
    def create_temporal_features(df, datetime_col="Datetime"):
        """Create temporal features from datetime column."""
        if datetime_col not in df.columns:
            return df

        df = df.copy()
        df[datetime_col] = pd.to_datetime(df[datetime_col])

        df["Hour"] = df[datetime_col].dt.hour
        df["Day of Week"] = df[datetime_col].dt.dayofweek
        df["Month"] = df[datetime_col].dt.month
        df["Day of Month"] = df[datetime_col].dt.day
        df["Quarter"] = df[datetime_col].dt.quarter
        df["Is Weekend"] = df["Day of Week"].isin([5, 6]).astype(int)

        return df

    @staticmethod
    def normalize_numeric_features(df):
        """Normalize numeric features to 0-1 range."""
        df = df.copy()
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df[numeric_cols] = (df[numeric_cols] - df[numeric_cols].min()) / (df[numeric_cols].max() - df[numeric_cols].min())
        return df

    @staticmethod
    def encode_categorical_features(df):
        """Encode categorical features."""
        df = df.copy()
        categorical_cols = df.select_dtypes(include=["object"]).columns
        df = pd.get_dummies(df, columns=categorical_cols, drop_first=True)
        return df

    @staticmethod
    def create_lag_features(df, target_col, lags=None):
        """Create lag features for time series."""
        if lags is None:
            lags = [1, 24]
        df = df.copy()
        for lag in lags:
            df[f"{target_col}_lag_{lag}"] = df[target_col].shift(lag)
        return df

    @staticmethod
    def create_rolling_features(df, target_col, windows=None):
        """Create rolling window features."""
        if windows is None:
            windows = [6, 24]
        df = df.copy()
        for window in windows:
            df[f"{target_col}_rolling_mean_{window}"] = df[target_col].rolling(window).mean()
            df[f"{target_col}_rolling_std_{window}"] = df[target_col].rolling(window).std()
        return df
