import json
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parent / "data"
DATA_DIR.mkdir(exist_ok=True)


def load_data(filename):
    path = DATA_DIR / filename

    if not path.exists():
        return []

    try:
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)

        if isinstance(data, dict):
            return list(data.values())

        return data if isinstance(data, list) else []

    except (json.JSONDecodeError, OSError):
        return []


def save_data(filename, data):
    path = DATA_DIR / filename
    temporary_path = path.with_suffix(".tmp")

    with open(temporary_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

    temporary_path.replace(path)
