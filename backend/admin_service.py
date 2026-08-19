import sqlite3
from pathlib import Path
from typing import Dict
from database.init_db import DB_PATH


def get_connection():
    return sqlite3.connect(DB_PATH)


def get_totals() -> Dict[str, int]:
    """Return total users and total predictions counts."""
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT COUNT(*) FROM Users")
    total_users = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM Predictions")
    total_predictions = cursor.fetchone()[0]

    connection.close()
    return {"total_users": total_users, "total_predictions": total_predictions}
