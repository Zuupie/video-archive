import os
import shutil
from pathlib import Path
import datetime
import re
import sys

# Pfad zur EXE, falls gebaut, sonst zum Skript
if getattr(sys, 'frozen', False):
    BASE_DIR = Path(sys.executable).parent
else:
    BASE_DIR = Path(__file__).parent

DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)  # wichtig, sonst kann sqlite nicht erstellen
ARCHIVE_ROOT = DATA_DIR / "archive"
ARCHIVE_ROOT.mkdir(parents=True, exist_ok=True)

MAX_NAME_LEN = 120

def save_video_and_thumbnail(video_path, thumbnail_path, data):
    ARCHIVE_ROOT.mkdir(parents=True, exist_ok=True)

    # Ordner nach Video & Thumbnail erstellen
    video_folder = ARCHIVE_ROOT / "videos"
    video_folder.mkdir(exist_ok=True)
    thumb_folder = ARCHIVE_ROOT / "thumbnails"
    thumb_folder.mkdir(exist_ok=True)

    # neuen Dateinamen erzeugen
    title = f"{data["date"]}_{data["title"]}" 
    new_name = safe_filename(title)

    # Video kopieren
    new_video_path = video_folder / (new_name + Path(video_path).suffix)
    shutil.copy(video_path, new_video_path)

    # Thumbnail kopieren
    if thumbnail_path != "":
        new_thumb_path = thumb_folder / (new_name + Path(thumbnail_path).suffix)
        shutil.copy(thumbnail_path, new_thumb_path)
    else:
        new_thumb_path = ""

    return str(new_video_path), str(new_thumb_path)


def safe_filename(title: str) -> str:
    name = title.lower()
    name = re.sub(r"[^\w\s-]", "", name)   # Sonderzeichen raus
    name = re.sub(r"\s+", "_", name)       # Leerzeichen -> _
    name = name.strip("_")

    name = name[:MAX_NAME_LEN]              # hart kürzen

    return name

