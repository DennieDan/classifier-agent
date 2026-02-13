"""SQLite database for conversation permits (name, prompt, response)."""

import os
import sqlite3
from typing import Optional

_SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
_DB_DIR = os.path.join(_SCRIPT_DIR, "data")
_DB_PATH = os.path.join(_DB_DIR, "conversations.db")


def _get_conn() -> sqlite3.Connection:
    return sqlite3.connect(_DB_PATH)


def init_db() -> None:
    """Create the data directory and permits table if they do not exist."""
    os.makedirs(_DB_DIR, exist_ok=True)
    conn = _get_conn()
    try:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS permits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                prompt TEXT NOT NULL,
                response TEXT NOT NULL
            )
            """
        )
        conn.commit()
        # Add messages_snapshot column if missing (migration)
        cur = conn.execute("PRAGMA table_info(permits)")
        columns = [row[1] for row in cur.fetchall()]
        if "messages_snapshot" not in columns:
            conn.execute("ALTER TABLE permits ADD COLUMN messages_snapshot TEXT")
            conn.commit()
    finally:
        conn.close()


def list_conversations() -> list[tuple[int, str]]:
    """Return (id, name) for all permits, ordered by id descending (newest first)."""
    conn = _get_conn()
    try:
        cur = conn.execute("SELECT id, name FROM permits ORDER BY id DESC")
        return cur.fetchall()
    finally:
        conn.close()


def get_conversation(permit_id: int) -> Optional[tuple[int, str, str, str]]:
    """Return (id, name, prompt, response) for the given id, or None if not found."""
    conn = _get_conn()
    try:
        cur = conn.execute(
            "SELECT id, name, prompt, response FROM permits WHERE id = ?",
            (permit_id,),
        )
        return cur.fetchone()
    finally:
        conn.close()


def insert_conversation(name: str, prompt: str, response: str = "") -> int:
    """Insert a row and return its id."""
    conn = _get_conn()
    try:
        cur = conn.execute(
            "INSERT INTO permits (name, prompt, response) VALUES (?, ?, ?)",
            (name, prompt, response),
        )
        conn.commit()
        return cur.lastrowid
    finally:
        conn.close()


def update_response(permit_id: int, response: str) -> None:
    """Update the response column for the given permit id."""
    conn = _get_conn()
    try:
        conn.execute(
            "UPDATE permits SET response = ? WHERE id = ?",
            (response, permit_id),
        )
        conn.commit()
    finally:
        conn.close()


def update_name(permit_id: int, name: str) -> None:
    """Update the name column for the given permit id."""
    conn = _get_conn()
    try:
        conn.execute(
            "UPDATE permits SET name = ? WHERE id = ?",
            (name.strip() or "Untitled", permit_id),
        )
        conn.commit()
    finally:
        conn.close()


def get_messages_snapshot(permit_id: int) -> Optional[str]:
    """Return the messages_snapshot JSON string for the given permit id, or None."""
    conn = _get_conn()
    try:
        cur = conn.execute(
            "SELECT messages_snapshot FROM permits WHERE id = ?",
            (permit_id,),
        )
        row = cur.fetchone()
        return row[0] if row and row[0] else None
    finally:
        conn.close()


def update_messages_snapshot(permit_id: int, messages_json: str) -> None:
    """Update the messages_snapshot column for the given permit id."""
    conn = _get_conn()
    try:
        conn.execute(
            "UPDATE permits SET messages_snapshot = ? WHERE id = ?",
            (messages_json, permit_id),
        )
        conn.commit()
    finally:
        conn.close()


def delete_conversation(permit_id: int) -> None:
    """Delete the conversation (permit) with the given id."""
    conn = _get_conn()
    try:
        conn.execute("DELETE FROM permits WHERE id = ?", (permit_id,))
        conn.commit()
    finally:
        conn.close()
