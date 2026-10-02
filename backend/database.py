import json
import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "criminal_network.db"
DATA_PATH = BASE_DIR / "data" / "demo_data.json"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS entities (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS relationships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            target TEXT NOT NULL,
            type TEXT NOT NULL,
            weight INTEGER DEFAULT 1
        )
    """)

    connection.commit()

    cursor.execute("SELECT COUNT(*) FROM entities")
    count = cursor.fetchone()[0]

    if count == 0:
        load_demo_data(connection)

    connection.close()


def load_demo_data(connection):
    with open(DATA_PATH, "r", encoding="utf-8") as file:
        data = json.load(file)

    for entity in data["entities"]:
        connection.execute(
            """
            INSERT INTO entities (id, name, type)
            VALUES (?, ?, ?)
            """,
            (
                entity["id"],
                entity["name"],
                entity["type"]
            )
        )

    for relationship in data["relationships"]:
        connection.execute(
            """
            INSERT INTO relationships
            (source, target, type, weight)
            VALUES (?, ?, ?, ?)
            """,
            (
                relationship["source"],
                relationship["target"],
                relationship["type"],
                relationship["weight"]
            )
        )

    connection.commit()


def get_entities():
    connection = get_connection()

    rows = connection.execute(
        "SELECT * FROM entities"
    ).fetchall()

    connection.close()

    return [dict(row) for row in rows]


def get_relationships():
    connection = get_connection()

    rows = connection.execute(
        "SELECT source, target, type, weight FROM relationships"
    ).fetchall()

    connection.close()

    return [dict(row) for row in rows]
