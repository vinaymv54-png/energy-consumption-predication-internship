# Energy Consumption Prediction Using ML

This project predicts energy consumption using historical energy usage data and influencing factors such as weather, time of day, occupancy, and appliance usage.

## Project Structure

- `data/raw/` - place raw CSV dataset files.
- `data/processed/` - cleaned CSV output after preprocessing.
- `notebooks/eda.ipynb` - exploratory data analysis notebook.
- `src/data_preprocessing.py` - raw data loading and cleaning logic.
- `src/feature_engineering.py` - feature extraction, encoding, scaling, and selection.
- `src/train_models.py` - model training and cross-validation.
- `src/evaluate_models.py` - model evaluation and comparison.
- `src/predict.py` - prediction for new/unseen samples.
- `models/` - saved `.joblib` model files.
- `app/streamlit_app.py` - optional Streamlit deployment UI.
- `report/project_report_template.md` - template for the final project report.
- `requirements.txt` - Python package dependencies.

## Setup

1. Create and activate a virtual environment:

```powershell
python -m venv venv
venv\Scripts\activate
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

## Usage

1. Place your raw dataset CSV in `data/raw/energy_data.csv`.
2. Run preprocessing:

```powershell
python src/data_preprocessing.py
```

3. After confirming column names and editing `src/feature_engineering.py`, run feature engineering, training, evaluation, and prediction scripts as needed.

## Notes

- The current preprocessing script uses a generic approach. Confirm your dataset's datetime and target column names before editing feature engineering.
- The final workflow should include training, evaluating, and saving the best model for later predictions.

## Technologies & Tools

- Programming Language: Python
- Development Environment: Jupyter Notebook, Google Colab, or Visual Studio Code
- Data Storage: CSV files
- Data Manipulation: `pandas`, `numpy`
- Visualization / EDA: `matplotlib`, `seaborn`
- Machine Learning: `scikit-learn`
- Advanced Modeling: `xgboost`
- Model Serialization: `joblib`
- Deployment / User Interface: `streamlit`
- Database: SQLite for authentication and prediction history
- Backend: Python service modules for user auth, prediction storage, and analytics
