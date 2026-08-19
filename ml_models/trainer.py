"""Machine Learning models training and evaluation utilities."""

import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
from xgboost import XGBRegressor


class MLModels:
    """Machine Learning models for energy prediction."""

    def __init__(self, random_state=42):
        """Initialize ML models."""
        self.random_state = random_state
        self.models = {
            "Linear Regression": LinearRegression(),
            "Decision Tree": DecisionTreeRegressor(random_state=random_state),
            "Random Forest": RandomForestRegressor(n_estimators=200, random_state=random_state),
            "XGBoost": XGBRegressor(n_estimators=100, random_state=random_state, verbose=0),
        }
        self.trained_models = {}
        self.metrics = {}

    def train_all_models(self, X_train, y_train):
        """Train all models."""
        for name, model in self.models.items():
            model.fit(X_train, y_train)
            self.trained_models[name] = model

    def evaluate_all_models(self, X_test, y_test):
        """Evaluate all models and store metrics."""
        for name, model in self.trained_models.items():
            y_pred = model.predict(X_test)
            r2 = r2_score(y_test, y_pred)
            mae = mean_absolute_error(y_test, y_pred)
            mse = mean_squared_error(y_test, y_pred)
            rmse = np.sqrt(mse)

            self.metrics[name] = {
                "R2": r2,
                "MAE": mae,
                "MSE": mse,
                "RMSE": rmse,
            }

    def get_best_model(self):
        """Get the best performing model based on R² score."""
        if not self.metrics:
            return None
        best_model_name = max(self.metrics, key=lambda x: self.metrics[x]["R2"])
        return best_model_name

    def save_model(self, model_name, path):
        """Save a trained model to disk."""
        if model_name in self.trained_models:
            joblib.dump(self.trained_models[model_name], path)
            return True
        return False

    def load_model(self, path):
        """Load a trained model from disk."""
        return joblib.load(path)

    def predict(self, model_name, X):
        """Make predictions using a specific model."""
        if model_name in self.trained_models:
            return self.trained_models[model_name].predict(X)
        return None

    def get_metrics_dataframe(self):
        """Get metrics as a pandas DataFrame."""
        df = pd.DataFrame(self.metrics).T
        df = df.round(4)
        return df.sort_values("R2", ascending=False)


def get_feature_importance(model, feature_names):
    """Get feature importance for tree-based models."""
    if hasattr(model, "feature_importances_"):
        importances = model.feature_importances_
        feature_importance_df = pd.DataFrame({
            "Feature": feature_names,
            "Importance": importances,
        }).sort_values("Importance", ascending=False)
        return feature_importance_df
    return None
