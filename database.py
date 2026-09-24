import sqlite3
from datetime import datetime

DB_NAME = "supportpulse.db"


def get_connection():
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    connection = get_connection()

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS incidents (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            application TEXT NOT NULL,
            priority TEXT NOT NULL,
            status TEXT NOT NULL,
            root_cause TEXT,
            resolution TEXT,
            created_at TEXT NOT NULL
        )
        """
    )

    connection.commit()
    connection.close()


def save_incident(title, application, priority, status, root_cause, resolution):
    connection = get_connection()

    connection.execute(
        """
        INSERT INTO incidents
        (title, application, priority, status, root_cause, resolution, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            title,
            application,
            priority,
            status,
            root_cause,
            resolution,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        ),
    )

    connection.commit()
    connection.close()


def get_incidents():
    connection = get_connection()

    rows = connection.execute(
        """
        SELECT id, title, application, priority, status,
               root_cause, resolution, created_at
        FROM incidents
        ORDER BY id DESC
        """
    ).fetchall()

    connection.close()

    return [dict(row) for row in rows]
