"""Prediction service module for managing prediction records in the database."""
import json
import sqlite3
from datetime import datetime
from typing import Dict, List

from database.init_db import DB_PATH


def get_connection():
    """Get a connection to the SQLite database."""
    return sqlite3.connect(DB_PATH)


def save_prediction(user_id: int, input_values: Dict[str, float], prediction: float) -> None:
    """Save a prediction record for the specified user."""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO Predictions "
        "(user_id, datetime, input_values, prediction) VALUES (?, ?, ?, ?)",
        (
            user_id,
            datetime.utcnow().isoformat(),
            json.dumps(input_values),
            float(prediction),
        ),
    )
    connection.commit()
    connection.close()


def get_predictions_for_user(user_id: int) -> List[Dict[str, str]]:
    """Retrieve prediction history for a user."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT id, datetime, input_values, prediction FROM Predictions "
        "WHERE user_id = ? ORDER BY datetime DESC",
        (user_id,),
    )
    rows = cursor.fetchall()
    connection.close()

    history = []
    for row in rows:
        history.append(
            {
                "id": row[0],
                "datetime": row[1],
                "input_values": json.loads(row[2]),
                "prediction": row[3],
            }
        )
    return history


def delete_prediction(prediction_id: int, user_id: int) -> bool:
    """Delete a prediction record belonging to a user."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "DELETE FROM Predictions WHERE id = ? AND user_id = ?",
        (prediction_id, user_id),
    )
    connection.commit()
    deleted = cursor.rowcount > 0
    connection.close()
    return deleted
