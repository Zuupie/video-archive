import sqlite3
import os
import sys
from pathlib import Path

# Pfad zur EXE, falls gebaut, sonst zum Skript
if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys.executable).parent
else:
    BASE_DIR = Path(__file__).parent

# Datenordner erstellen
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)  # wichtig, sonst kann sqlite nicht erstellen

DB_PATH = DATA_DIR / "videos.db"

def init_db():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS videos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            description TEXT,
            note TEXT,
            category TEXT,
            date TEXT,
            video_path TEXT,
            thumbnail_path TEXT
        )
    """)

    conn.commit()
    conn.close()


def insert_video(data):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        INSERT INTO videos (title, description, note, category, date, video_path, thumbnail_path)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        data["title"],
        data["description"],
        data["note"],
        data["category"],
        data["date"],
        data["video_path"],
        data["thumbnail_path"]
    ))

    conn.commit()
    conn.close()


def get_all_videos():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("SELECT * FROM videos ORDER BY date DESC")
    rows = c.fetchall()

    conn.close()
    return rows
