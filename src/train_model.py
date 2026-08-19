import joblib
import math
import pandas as pd
from pathlib import Path
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


def load_feature_data(file_path: Path) -> pd.DataFrame:
    """Load engineered feature data from CSV."""
    return pd.read_csv(file_path, parse_dates=["Datetime"])


def prepare_data(df: pd.DataFrame):
    """Split features and target from the engineered dataset."""
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


def train_random_forest(X, y):
    """Train a Random Forest Regressor on the data."""
    model = RandomForestRegressor(random_state=42, n_estimators=200)
    model.fit(X, y)
    return model


def evaluate_model(model, X, y):
    """Compute evaluation metrics for the trained model."""
    predictions = model.predict(X)
    mae = mean_absolute_error(y, predictions)
    mse = mean_squared_error(y, predictions)
    rmse = math.sqrt(mse)
    r2 = r2_score(y, predictions)
    return mae, rmse, r2


def main() -> None:
    project_root = Path(__file__).resolve().parent.parent
    feature_data_path = project_root / "data" / "processed" / "AEP_hourly_features.csv"
    model_path = project_root / "models" / "random_forest_aep.joblib"

    df_features = load_feature_data(feature_data_path)
    X, y = prepare_data(df_features)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, shuffle=False
    )

    model = train_random_forest(X_train, y_train)
    joblib.dump(model, model_path)
    print(f"Saved trained Random Forest model to: {model_path}")

    mae, rmse, r2 = evaluate_model(model, X_test, y_test)
    print("Evaluation on test set:")
    print(f"MAE: {mae:.2f}")
    print(f"RMSE: {rmse:.2f}")
    print(f"R2: {r2:.4f}")


if __name__ == "__main__":
    main()
