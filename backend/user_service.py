import sqlite3
from pathlib import Path
from typing import Optional, Dict
from utils.security import hash_password, verify_password
from database.init_db import DB_PATH


def get_connection():
     return sqlite3.connect(DB_PATH)


def create_user(username: str, email: str, password: str) -> bool:
    """Create a new user if the email is not already taken."""
    password_hash = hash_password(password)
    connection = get_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(
            "INSERT INTO Users (username, email, password_hash) VALUES (?, ?, ?)",
            (username, email, password_hash),
        )
        connection.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        connection.close()


def get_user_by_identifier(identifier: str) -> Optional[Dict[str, str]]:
    """Retrieve a user record by email or username."""
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT id, username, email, password_hash FROM Users WHERE email = ? OR username = ?",
        (identifier, identifier),
    )
    row = cursor.fetchone()
    connection.close()

    if row:
        return {
            "id": row[0],
            "username": row[1],
            "email": row[2],
            "password_hash": row[3],
        }
    return None


def authenticate_user(identifier: str, password: str) -> Optional[Dict[str, str]]:
    """Verify a user's email or username and password."""
    user = get_user_by_identifier(identifier)
    if user and verify_password(password, user["password_hash"]):
        return user
    return None
