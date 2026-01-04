import sqlite3
from passlib.hash import pbkdf2_sha256

DB_NAME = "users.db"

def get_connection():
    return sqlite3.connect(DB_NAME, check_same_thread=False)

# Create users table if not exists
def create_users_table():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
        """
    )
    conn.commit()
    conn.close()

create_users_table()


# -----------------------------
#  SIGNUP FUNCTION
# -----------------------------
def signup(name, email, password):
    conn = get_connection()
    cursor = conn.cursor()

    # Hash password
    hashed_password = pbkdf2_sha256.hash(password)

    try:
        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
            (name, email, hashed_password),
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        # email already exists
        return False
    finally:
        conn.close()


# -----------------------------
#  LOGIN FUNCTION
# -----------------------------
def login(email, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    conn.close()

    if user and pbkdf2_sha256.verify(password, user[3]):
        return user
    return None
