import json
import os
import time

from config import DATA_DIR, SAVE_PATH


def default_progress():
    return {
        "settings": {
            "volume": 0.6,
            "difficulty_bias": "normal",
            "voice_input": True,
            "voice_output": True,
            "voice_volume": 0.8,
        },
        "stats": {},
        "totals": {"correct": 0, "wrong": 0, "stars": 0},
        "sessions": [],
    }


def _ensure_structure(progress):
    progress.setdefault("settings", {})
    settings = progress["settings"]
    settings.setdefault("volume", 0.6)
    settings.setdefault("difficulty_bias", "normal")
    settings.setdefault("voice_input", True)
    settings.setdefault("voice_output", True)
    settings.setdefault("voice_volume", 0.8)
    progress.setdefault("stats", {})
    progress.setdefault("totals", {"correct": 0, "wrong": 0, "stars": 0})
    progress.setdefault("sessions", [])
    return progress


def load_progress():
    if not os.path.exists(SAVE_PATH):
        return default_progress()
    try:
        with open(SAVE_PATH, "r", encoding="utf-8") as handle:
            progress = json.load(handle)
    except (json.JSONDecodeError, OSError) as exc:
        print(f"Progress file could not be read: {exc}")
        return default_progress()
    return _ensure_structure(progress)


def save_progress(progress):
    os.makedirs(DATA_DIR, exist_ok=True)
    progress["last_saved"] = time.time()
    with open(SAVE_PATH, "w", encoding="utf-8") as handle:
        json.dump(progress, handle, indent=2)
