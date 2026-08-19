import joblib
import pandas as pd
from pathlib import Path


def load_model() -> object:
    """Load the saved Random Forest model."""
    model_path = Path(__file__).resolve().parent.parent / "models" / "random_forest_aep.joblib"
    return joblib.load(model_path)


def load_scaler() -> object:
    """Load the saved feature scaler."""
    scaler_path = Path(__file__).resolve().parent.parent / "models" / "feature_scaler.joblib"
    return joblib.load(scaler_path)


def prepare_input(payload: dict) -> pd.DataFrame:
    """Prepare a feature DataFrame from user input."""
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
    df = pd.DataFrame([payload])
    return df[feature_columns]


def predict_energy(payload: dict) -> float:
    """Predict energy consumption from user input."""
    model = load_model()
    scaler = load_scaler()
    input_df = prepare_input(payload)
    input_df[ input_df.columns ] = scaler.transform(input_df[input_df.columns])
    prediction = model.predict(input_df)
    return float(prediction[0])
