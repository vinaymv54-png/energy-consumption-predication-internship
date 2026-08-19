import joblib
import pandas as pd
from pathlib import Path
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def load_feature_data(file_path: Path) -> pd.DataFrame:
    """Load engineered feature data from CSV."""
    return pd.read_csv(file_path, parse_dates=["Datetime"])


def prepare_data(df: pd.DataFrame):
    """Prepare X and y for evaluation."""
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
    X = df[feature_columns]
    y = df["AEP_MW"]
    return X, y


def evaluate_metrics(y_true, y_pred):
    """Compute regression metrics."""
    mae = mean_absolute_error(y_true, y_pred)
    mse = mean_squared_error(y_true, y_pred)
    rmse = mse ** 0.5
    r2 = r2_score(y_true, y_pred)
    return mae, rmse, r2


def main() -> None:
    project_root = Path(__file__).resolve().parent.parent
    feature_data_path = project_root / "data" / "processed" / "AEP_hourly_features.csv"
    model_path = project_root / "models" / "random_forest_aep.joblib"

    df_features = load_feature_data(feature_data_path)
    X, y = prepare_data(df_features)

    if not model_path.exists():
        raise FileNotFoundError(f"Trained model not found at {model_path}")

    model = joblib.load(model_path)
    predictions = model.predict(X)
    mae, rmse, r2 = evaluate_metrics(y, predictions)

    print("Evaluation for the full feature dataset:")
    print(f"MAE: {mae:.2f}")
    print(f"RMSE: {rmse:.2f}")
    print(f"R2: {r2:.4f}")

    pd.DataFrame({"actual": y, "predicted": predictions}).to_csv(
        project_root / "data" / "processed" / "evaluation_actual_vs_predicted.csv",
        index=False,
    )
    print("Saved actual vs predicted comparison to data/processed/evaluation_actual_vs_predicted.csv")


if __name__ == "__main__":
    main()
