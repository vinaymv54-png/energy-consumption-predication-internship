import argparse
import joblib
import pandas as pd
from pathlib import Path


def load_model(model_path: Path):
    """Load the trained Random Forest model."""
    return joblib.load(model_path)


def load_scaler(scaler_path: Path):
    """Load the scaler used during feature engineering."""
    return joblib.load(scaler_path)


def create_input_dataframe(sample: dict) -> pd.DataFrame:
    """Convert a dict input into a feature DataFrame."""
    return pd.DataFrame([sample])


def load_sample_csv(file_path: Path) -> pd.DataFrame:
    """Load a small CSV file containing feature columns for prediction."""
    return pd.read_csv(file_path)


def predict(model, scaler, df: pd.DataFrame) -> pd.Series:
    """Scale raw sample features and return model predictions."""
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
    df_scaled = df.copy()
    df_scaled[feature_columns] = scaler.transform(df_scaled[feature_columns])
    return model.predict(df_scaled[feature_columns])


def main() -> None:
    parser = argparse.ArgumentParser(description="Predict hourly energy consumption for AEP data.")
    parser.add_argument("--input_csv", type=str, help="Optional CSV file with sample rows to predict.")
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parent.parent
    model_path = project_root / "models" / "random_forest_aep.joblib"
    scaler_path = project_root / "models" / "feature_scaler.joblib"

    if not model_path.exists():
        raise FileNotFoundError(f"Trained model not found at {model_path}")
    if not scaler_path.exists():
        raise FileNotFoundError(f"Scaler not found at {scaler_path}")

    model = load_model(model_path)
    scaler = load_scaler(scaler_path)

    if args.input_csv:
        sample_df = load_sample_csv(Path(args.input_csv))
    else:
        sample_df = create_input_dataframe(
            {
                "hour": 12,
                "day_of_week": 2,
                "month": 6,
                "is_weekend": 0,
                "lag_1": 14000.0,
                "lag_24": 15000.0,
                "rolling_6": 14500.0,
                "rolling_24": 14800.0,
            }
        )

    predictions = predict(model, scaler, sample_df)
    for idx, value in enumerate(predictions, start=1):
        print(f"Sample {idx}: predicted AEP_MW = {value:.2f}")


if __name__ == "__main__":
    main()
