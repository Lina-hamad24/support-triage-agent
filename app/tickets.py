import sqlite3
from datetime import datetime


DB_PATH = "tickets.db"


def create_ticket(question: str) -> int:
    connection = sqlite3.connect(DB_PATH)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            question TEXT NOT NULL,
            status TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    cursor.execute(
        """
        INSERT INTO tickets (question, status, created_at)
        VALUES (?, ?, ?)
        """,
        (
            question,
            "open",
            datetime.now().isoformat(),
        ),
    )

    ticket_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return ticket_id