import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "app.db"


def init_db() -> None:
    """Initialize the SQLite database with the required tables."""
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS Predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            datetime TEXT NOT NULL,
            input_values TEXT NOT NULL,
            prediction REAL NOT NULL,
            FOREIGN KEY(user_id) REFERENCES Users(id)
        )
        """
    )

    connection.commit()
    connection.close()


if __name__ == "__main__":
    init_db()
    print(f"Database initialized at {DB_PATH}")
