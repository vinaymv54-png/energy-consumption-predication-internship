"""Feature engineering module for creating time-series features from energy data."""
from pathlib import Path

import joblib
import pandas as pd
from sklearn.preprocessing import StandardScaler


def load_clean_data(file_path: Path) -> pd.DataFrame:
    """Load cleaned energy data from CSV."""
    return pd.read_csv(file_path, parse_dates=["Datetime"])


def engineer_features(df: pd.DataFrame) -> (pd.DataFrame, StandardScaler):
    """Create time-series features for energy prediction.

    Args:
        df: Cleaned DataFrame with columns Datetime and AEP_MW.

    Returns:
        Tuple containing the feature DataFrame and fitted scaler.
    """
    df = df.sort_values("Datetime").reset_index(drop=True).copy()

    df["hour"] = df["Datetime"].dt.hour
    df["day_of_week"] = df["Datetime"].dt.dayofweek
    df["month"] = df["Datetime"].dt.month
    df["is_weekend"] = df["day_of_week"].isin([5, 6]).astype(int)

    df["lag_1"] = df["AEP_MW"].shift(1)
    df["lag_24"] = df["AEP_MW"].shift(24)
    df["rolling_6"] = df["AEP_MW"].rolling(window=6, min_periods=1).mean()
    df["rolling_24"] = df["AEP_MW"].rolling(window=24, min_periods=1).mean()

    df = df.dropna().reset_index(drop=True)

    feature_columns = [
        "hour",
        "day_of_week",
        "month",
        "is_weekend",
        "lag_1",
        "lag_24",
        "rolling_6",
        "rolling_24",
    ]

    scaler = StandardScaler()
    df[feature_columns] = scaler.fit_transform(df[feature_columns])

    return df, scaler


def save_feature_data(df: pd.DataFrame, output_path: Path) -> None:
    """Save engineered features to disk."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)


def save_scaler(scaler: StandardScaler, output_path: Path) -> None:
    """Save the fitted scaler so predictions can use the same feature scaling."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(scaler, output_path)


def main() -> None:
    """Load cleaned data, engineer features, and save results to disk."""
    project_root = Path(__file__).resolve().parent.parent
    clean_path = project_root / "data" / "processed" / "AEP_hourly_clean.csv"
    features_path = project_root / "data" / "processed" / "AEP_hourly_features.csv"
    scaler_path = project_root / "models" / "feature_scaler.joblib"

    df_clean = load_clean_data(clean_path)
    df_features, scaler = engineer_features(df_clean)
    save_feature_data(df_features, features_path)
    save_scaler(scaler, scaler_path)
    print(f"Saved engineered features to: {features_path}")
    print(f"Saved scaler to: {scaler_path}")


if __name__ == "__main__":
    main()
