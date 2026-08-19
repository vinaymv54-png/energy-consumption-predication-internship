"""Data preprocessing module for cleaning and normalizing energy datasets."""
from pathlib import Path

import pandas as pd


def load_raw_data(file_path: Path) -> pd.DataFrame:
    """Load the raw dataset from CSV."""
    return pd.read_csv(file_path)


def normalize_schema(df: pd.DataFrame) -> pd.DataFrame:
    """Normalize the uploaded dataset to the project's expected columns."""
    df = df.copy()

    if "Datetime" in df.columns and "AEP_MW" in df.columns:
        return df

    if {"Date", "Time"}.issubset(df.columns) and "Energy_Consumption_kWh" in df.columns:
        df["Datetime"] = pd.to_datetime(
            df["Date"].astype(str) + " " + df["Time"].astype(str),
            errors="coerce",
        )
        df = df.rename(columns={"Energy_Consumption_kWh": "AEP_MW"})
        df = df[["Datetime", "AEP_MW"]].copy()
        return df

    raise ValueError(
        "Expected either Datetime/AEP_MW columns or "
        "Date/Time/Energy_Consumption_kWh columns."
    )


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean the raw dataset.

    Steps:
    - drop duplicates
    - parse the Datetime column
    - fill missing target values with the median
    - sort chronologically
    - remove extreme outliers in the target using IQR
    """
    df = df.drop_duplicates().copy()
    df = normalize_schema(df)

    if "Datetime" not in df.columns or "AEP_MW" not in df.columns:
        raise ValueError("Expected columns 'Datetime' and 'AEP_MW' in the raw dataset.")

    df["Datetime"] = pd.to_datetime(df["Datetime"], errors="coerce")
    df = df[df["Datetime"].notna()].copy()
    df = df.sort_values("Datetime").reset_index(drop=True)

    df["AEP_MW"] = pd.to_numeric(df["AEP_MW"], errors="coerce")
    if df["AEP_MW"].isna().any():
        df["AEP_MW"] = df["AEP_MW"].fillna(df["AEP_MW"].median())

    q1 = df["AEP_MW"].quantile(0.25)
    q3 = df["AEP_MW"].quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    df = df[(df["AEP_MW"] >= lower_bound) & (df["AEP_MW"] <= upper_bound)].copy()

    return df


def save_clean_data(df: pd.DataFrame, output_path: Path) -> None:
    """Save cleaned data to a CSV file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False)


def main() -> None:
    """Load raw data, clean it, and save to processed directory."""
    project_root = Path(__file__).resolve().parent.parent
    raw_candidates = [
        project_root / "data" / "raw" / "energy_consumption_dataset_600_rows_historical.csv",
        project_root / "data" / "raw" / "AEP_hourly.csv",
    ]
    raw_path = next((path for path in raw_candidates if path.exists()), raw_candidates[0])
    clean_path = project_root / "data" / "processed" / "AEP_hourly_clean.csv"

    df_raw = load_raw_data(raw_path)
    df_clean = clean_data(df_raw)
    save_clean_data(df_clean, clean_path)
    print(f"Loaded raw dataset from: {raw_path}")
    print(f"Saved cleaned dataset to: {clean_path}")


if __name__ == "__main__":
    main()
