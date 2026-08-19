from .init_db import DB_PATH, init_db

# Ensure the database schema exists when the database package is imported.
init_db()
