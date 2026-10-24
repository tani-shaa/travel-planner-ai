"""
SQLite-based trip persistence layer.
Zero external DB dependencies — uses Python's built-in sqlite3.
"""

import sqlite3
import json
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent.parent / "data" / "trips.db"


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with _connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS trips (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                name          TEXT NOT NULL,
                destination   TEXT NOT NULL,
                duration      INTEGER NOT NULL,
                budget        TEXT,
                pace          TEXT,
                travel_style  TEXT,
                interests     TEXT,
                itinerary     TEXT NOT NULL,
                preferences   TEXT,
                created_at    TEXT NOT NULL,
                updated_at    TEXT NOT NULL
            )
        """)
        conn.commit()


def save_trip(
    name: str,
    destination: str,
    duration: int,
    budget: str,
    pace: str,
    travel_style: str,
    interests: list,
    itinerary: dict,
    preferences: dict = None,
) -> int:
    init_db()
    now = datetime.utcnow().isoformat()
    with _connect() as conn:
        cur = conn.execute(
            """INSERT INTO trips
               (name, destination, duration, budget, pace, travel_style,
                interests, itinerary, preferences, created_at, updated_at)
               VALUES (?,?,?,?,?,?,?,?,?,?,?)""",
            (name, destination, duration, budget, pace, travel_style,
             json.dumps(interests), json.dumps(itinerary),
             json.dumps(preferences or {}), now, now),
        )
        conn.commit()
        return cur.lastrowid


def get_all_trips() -> list:
    init_db()
    with _connect() as conn:
        rows = conn.execute("SELECT * FROM trips ORDER BY created_at DESC").fetchall()
    result = []
    for row in rows:
        t = dict(row)
        t["interests"]   = json.loads(t["interests"]   or "[]")
        t["itinerary"]   = json.loads(t["itinerary"]   or "{}")
        t["preferences"] = json.loads(t["preferences"] or "{}")
        result.append(t)
    return result


def get_trip_by_id(trip_id: int) -> dict:
    init_db()
    with _connect() as conn:
        row = conn.execute("SELECT * FROM trips WHERE id=?", (trip_id,)).fetchone()
    if row is None:
        return None
    t = dict(row)
    t["interests"]   = json.loads(t["interests"]   or "[]")
    t["itinerary"]   = json.loads(t["itinerary"]   or "{}")
    t["preferences"] = json.loads(t["preferences"] or "{}")
    return t


def delete_trip(trip_id: int) -> None:
    init_db()
    with _connect() as conn:
        conn.execute("DELETE FROM trips WHERE id=?", (trip_id,))
        conn.commit()


def update_itinerary(trip_id: int, itinerary: dict) -> None:
    init_db()
    now = datetime.utcnow().isoformat()
    with _connect() as conn:
        conn.execute(
            "UPDATE trips SET itinerary=?, updated_at=? WHERE id=?",
            (json.dumps(itinerary), now, trip_id),
        )
        conn.commit()
